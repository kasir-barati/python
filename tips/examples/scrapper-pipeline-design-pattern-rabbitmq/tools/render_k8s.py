"""
Patches spec.maxReplicaCount in each worker's ScaledObject manifest from `instances` in the
pipeline YAML - the ceiling KEDA scales that stage up to under load (it always scales down to
minReplicaCount, 0 here, when idle; `instances` was never a keep-alive floor even in the original
thread-pool design).

Only that one field is touched - ruamel.yaml round-trips the rest of each file (formatting, comments,
any resource limits/probes added by hand) untouched. Run via `make sync-k8s`; `--check` reports drift
without writing, for CI.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml
from ruamel.yaml import YAML

REPO_ROOT = Path(__file__).parent.parent
PIPELINE_YAML = REPO_ROOT / "src" / "pipelines" / "wiki_yahoo_scraper_pipeline.yaml"
K8S_DIR = REPO_ROOT / "k8s"

yaml_roundtrip = YAML()
yaml_roundtrip.preserve_quotes = True
yaml_roundtrip.indent(mapping=2, sequence=4, offset=2)


def _service_name(worker_name: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "-", worker_name).lower()


def main() -> None:
    check_only = "--check" in sys.argv

    with open(PIPELINE_YAML) as in_file:
        pipeline_spec = yaml.safe_load(in_file)

    drift = False
    for worker in pipeline_spec["workers"]:
        if "input_queue" not in worker:
            continue  # one-shot producers (e.g. WikiWorker) run as a CronJob, not autoscaled

        manifest_path = K8S_DIR / f"{_service_name(worker['name'])}-scaledobject.yaml"
        manifest = yaml_roundtrip.load(manifest_path)

        wanted = worker.get("instances", 1)
        current = manifest["spec"]["maxReplicaCount"]
        if current == wanted:
            continue

        if check_only:
            print(f"{manifest_path}: maxReplicaCount is {current}, pipeline YAML says {wanted}")
            drift = True
            continue

        manifest["spec"]["maxReplicaCount"] = wanted
        yaml_roundtrip.dump(manifest, manifest_path)
        print(f"{manifest_path}: maxReplicaCount -> {wanted}")

    if drift:
        sys.exit(1)


if __name__ == "__main__":
    main()
