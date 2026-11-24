# Kubernetes + KEDA reference manifests

Reference design for how this pipeline should run in production — **written but not tested against a
live cluster** (this repo's dev loop is Docker Compose only). Treat these as a documented starting point,
not a deploy-ready artifact.

## Why this shape

Docker Compose has no concept of "scale to zero when idle, scale up when work arrives" — replica counts
in `compose.generated.yml` are fixed. In production that decision belongs to
[KEDA](https://keda.sh), which scales Deployments up/down (including to zero) based on the actual
RabbitMQ queue depth, not a guess made from inside a consumer about how long is "long enough" idle. See
the main [README](../README.md#no-poison-pill-propagation-and-no-self-timeout-either) for why the
workers themselves no longer self-terminate.

Mapping from Compose to this design:

| Compose (`compose.generated.yml`)     | Kubernetes                                    |
|----------------------------------------|------------------------------------------------|
| `wiki-worker` (one-shot, `restart: no`) | `CronJob` — reruns the scrape on a schedule    |
| `yahoo-finance-worker` (fixed replicas) | `Deployment` + `ScaledObject` (0–4 replicas)   |
| `postgres-worker` (fixed replicas)      | `Deployment` + `ScaledObject` (0–4 replicas)   |
| `.env` / `env_file`                     | `Secret` (`config-secret.yaml`)                |
| RabbitMQ / Postgres containers          | assumed to already exist in-cluster (or be managed services) — not included here |

`run_worker.py` and `WORKER_NAME` are unchanged — the same image and entrypoint run in every container
below, exactly as in Compose; only *what schedules/scales the container* differs.

## Prerequisites this assumes

- KEDA is installed: `helm install keda kedacore/keda --namespace keda --create-namespace`
- A `rabbitmq` Service and a `postgres` Service already exist in-cluster (or `PG_HOST`/`RABBITMQ_HOST`
  in `config-secret.yaml` point at managed instances instead).
- The image built from this repo's `Dockerfile` is pushed somewhere the cluster can pull it — replace
  every `your-registry/...` placeholder below.

## Files

- `config-secret.yaml` — placeholder values mirroring `.env.example`, plus `RABBITMQ_URL` (a full
  connection string) used only by KEDA's `TriggerAuthentication`, since the app itself reads the
  individual `RABBITMQ_*`/`POSTGRES_*` keys via `config.py`. **Do not commit real credentials here** —
  in a real cluster this comes from a secrets manager (e.g. External Secrets, Sealed Secrets), not a
  plain YAML file.
- `wiki-cronjob.yaml` — runs `WORKER_NAME=WikiWorker` on a schedule.
- `yahoo-finance-worker-deployment.yaml` / `postgres-worker-deployment.yaml` — start at `replicas: 0`;
  KEDA owns the replica count once its `ScaledObject` is applied.
- `rabbitmq-trigger-auth.yaml` — the `TriggerAuthentication` KEDA's RabbitMQ scaler uses to query queue
  depth.
- `yahoo-finance-worker-scaledobject.yaml` / `postgres-worker-scaledobject.yaml` — watch `SymbolQueue`
  / `PostgresUploading` respectively; `minReplicaCount: 0` so KEDA scales to zero when idle,
  `maxReplicaCount` is the ceiling KEDA scales that stage up to under load.

### Keeping `maxReplicaCount` in sync with the pipeline YAML

`instances` in `wiki_yahoo_scraper_pipeline.yaml` maps to `maxReplicaCount`, not `minReplicaCount` —
it's the capacity ceiling we've sized/tested for, not a floor to keep warm (a floor would defeat scaling
to zero). `../tools/render_k8s.py` patches only that field in each `*-scaledobject.yaml` from the
pipeline YAML, leaving everything else in the file (comments, any resource limits/probes added by hand)
untouched:

```bash
make sync-k8s   # patch maxReplicaCount from the pipeline YAML, write the result
make check-k8s  # same computation, no write - exits nonzero on drift, for CI
```

Wire `make check-k8s` into CI so a PR that bumps `instances` without re-running `make sync-k8s` (or
vice versa) fails the build instead of silently drifting.

`render_k8s.py` needs `ruamel.yaml` to round-trip these files without stripping their comments (plain
`pyyaml`, which the app itself uses at runtime, doesn't preserve comments on a load/dump cycle). That
package is declared under `[dependency-groups].dev` in `../pyproject.toml`, not `[project].dependencies`
— it's a tooling dependency for this script alone, nothing under `src/` imports it, and the `Dockerfile`
installs with `uv sync --no-dev` specifically so it never ends up in the image that actually runs in a
container. `make sync-k8s` / `make check-k8s` still work locally because `uv sync` (no flag, e.g. via
`make init`) installs the dev group by default.

Omitted for brevity, and worth adding before real use: resource requests/limits, liveness/readiness
probes, `PodDisruptionBudget`, and a `ServiceAccount` scoped to what each worker actually needs.
