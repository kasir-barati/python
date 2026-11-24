"""Generic entrypoint every worker container runs: given WORKER_NAME, reflectively resolve and
run the matching pipeline stage from the YAML, mirroring how the original YamlPipelineExecutor
instantiated worker classes via importlib instead of hardcoding them."""

from __future__ import annotations

import importlib
import os

from config import PIPELINE_YAML
from pipelines.reader import PipelineTopology


def main() -> None:
    worker_name = os.environ["WORKER_NAME"]
    topology = PipelineTopology(PIPELINE_YAML)
    spec = topology.worker(worker_name)
    worker_class = getattr(importlib.import_module(spec["location"]), spec["class"])
    worker_class(topology, worker_name).run()


if __name__ == "__main__":
    main()
