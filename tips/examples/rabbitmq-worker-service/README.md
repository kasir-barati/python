# Summary of the Example

I wrote about this and explain this here: dev.to post link

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
