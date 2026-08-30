# Summary of the Example

I wrote about this and explain this here: https://dev.to/kasir-barati/rabbitmq-consumer-as-a-separate-worker-service-adc

And in `tests/test_worker_integration.py` I am using `testcontainers` to boot real RabbitMQ, Redis, and Postgres containers and check two things:

1. **Happy path.** A published email is consumed, upserted into `users` via `UserRepository`, echoed to Redis, and acked (queue drained, not left pending).
2. **Crash recovery, without data corruption.** A worker that writes the user row and publishes to Redis, then crashes *before* acking, is simulated by killing its connection mid-flight. A second, independent `Worker` instance, standing in for a restarted replica, still receives the redelivered message and reprocesses it, and the test asserts there is still exactly **one** `users` row for that email, not two. That's `get_or_create`'s idempotency doing its job: at-least-once delivery plus an idempotent handler equals correct behavior even after a crash, entirely without the API process being restarted or even aware anything happened.

Durability of "the message survives a crash" comes from RabbitMQ fundamentals (a durable queue, a persistent message, manual ack); the "and it doesn't become a duplicate" half comes from the shared repository. The tests exist to prove the worker doesn't accidentally break either guarantee, not to re-test RabbitMQ or Postgres themselves.

## [GraphQL API](./api/schema.graphql)

The subscription API is the one that receives messages published from the worker.

## [Consumer](./worker/src/consumer.py)

```
              RabbitMQ consumer
                     │
                     ▼
       ┌─────▶ Wait for a message ◀──────────┐
       │             │                       │
       │      ┌──────┴─────────┐             │
       │      │                │             │
       │  message          1 second,         │
       │  arrives         no message         │
       │      │                │             │
       │      ▼                ▼             │
       │  _should_run?      method=None      │
       │      │                │             │
       │   ┌──┴─────┐          │             │
       │   │        │          │             │
       │  TRUE    FALSE        │             │
       │   │        │          │             │
       │   ▼        ▼          ▼             │
       │ process  break    continue ─────────┘
       │ message    │
       │   │        ▼
       └───┘     EXIT LOOP   
```

> [!TIP]
>
> RabbitMQ consumption is fundamentally event/stream based, not polling-based. This means that:
>
> ```py
> for method, properties, body in self._channel.consume(
>     self._queue_name,
>     inactivity_timeout=1,
> ):
> ```
>
> is NOT sending a new RabbitMQ network request every second in the same way that an application might repeatedly execute `SELECT ...` against PostgreSQL. Think of `consume()` as a long-lived connection.
>
> ```
>                       ┌─────────────────────┐
>                       │      RabbitMQ       │
>                       └──────────┬──────────┘
>                                  │
>                                  | persistent connection
>                                  │
>                                  ▼
>                       ┌─────────────────────┐
>                       │  channel.consume()  │
>                       └──────────┬──────────┘
>                                  │
>                                  |
>     ┌────────────────────▶ WAIT FOR EVENT
>     |                            ▼
>     |            ┌───────────────┴───────────────┐
>     |            │                               │
>     |     📩 MESSAGE ARRIVES              ⏰ 1 SEC PASSES
>     |            │                               │
>     |            ▼                               ▼
>     |        method != None                   method=None
>     |            │                               │
>     |            ▼                               ▼
>     |         process                         Should run?
>     |            │                               │
>     |            ▼                           ┌───┴───┐
>     |           ACK                         Yes      No (SIGTERM/SIGINT)
>     |            │                           │       |
>     |            └───────────────┬───────────┘       |
>     |                            │                   ▼
>     └────────────────────────────┘                EXIT LOOP
> ```

### Important Note About DB Transaction & Order of Actions

This is the current order which works wonderfully: `DB commit → Redis publish → RabbitMQ ack`

| Crash 💥            | Result                                                  |
| ------------------- | ------------------------------------------------------- |
| After DB commit     | Message gets redelivered, `get_or_create` is idempotent |
| After Redis publish | DB already exists; Redis event may be duplicated        |
| After RabbitMQ ack  | Everything done                                         |

> [!IMPORTANT]
>
> But now imagine the order would be: `Redis publish → DB commit → RabbitMQ ack` and after Redis publish but before DB commit our little consumer worker crashes. Then the **event says user exists, but DB transaction may roll back**.

So when we commit first the database transaction, we are making the database the source of truth:

- The users table is the authoritative record of which emails exist.
- ["At‑least‑once" delivery](https://www.systemoverflow.com/learn/design-fundamentals/communication-patterns/idempotency-at-least-once-delivery-and-the-outbox-inbox-pattern): This guarantees **eventual delivery** of the Redis notification without any data loss.

## [Shared Library](./shared)

`shared` is a real installable Python package (its own `pyproject.toml`, built with hatchling). The root `pyproject.toml` depends on it as a local path dependency:

```toml
[tool.uv.sources]
shared = { path = "shared", editable = true }
```

This is one source of truth for the `users` table and its `UserRepository`, versioned and deployed together with whichever service imports it, instead of drifting apart in two copies. In a repo split into `api-repo` and `worker-repo` instead, `shared` would be its own versioned package (private PyPI index, git dependency, whatever your org uses) rather than a local path — same principle, just resolved across repositories instead of across directories. Although honestly I would NOT recommend it since it would just makes the maintenance a ton harder. So if possible go for a monorepo.

See [`shared/README.md`](./shared/README.md) for how the package itself is laid out (`db/`, per-entity subpackages like `db/user/`, and why).

What `shared` alone doesn't solve is migrations, so this example wires up [Alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html) too, under [`shared/migrations`](./shared/migrations): `shared.db` owns the models and therefore the migration scripts, but only the API's deploy step runs them (`make db-migrate`, also baked into [`api/Dockerfile`](./api/Dockerfile)'s `CMD` ahead of `uvicorn`). Neither service calls `create_all` at startup anymore — see the comment in [`shared/db/engine.py`](./shared/src/shared/db/engine.py) — because two independently-deployed services racing to create/alter the same table is exactly the failure mode migrations exist to prevent.

That still leaves the real constraint on you as the schema author, not on any tooling here: because `api` and `worker` deploy independently, a schema change needs to be backward-compatible for the window where an old and a new version of either service might be running against the same database at once. Practically that means expand/contract instead of drop-and-recreate — e.g. add a new nullable column in one migration/release, backfill and dual-write from both old and new code paths, then only drop the old column in a later release once every replica has rolled forward.
