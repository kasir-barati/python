# Scraper Pipeline

A YAML-defined worker pipeline: `wiki.py` scrapes S&P 500 tickers, `yahoo_finance_price.py` fetches prices per ticker, `postgres.py` writes them to Postgres. `pipelines/reader.py` (`YamlPipelineExecutor`) reads `pipelines/wiki_yahoo_scraper_pipeline.yaml`, wires queues to workers, and drives shutdown.

## Topology

```mermaid
flowchart LR
    subgraph WikiWorker["WikiWorker (1 instance)"]
        W1[WikiWorkerMasterScheduler]
    end
    subgraph YahooFinanceWorker["YahooFinanceWorker (4 instances)"]
        Y1[Thread 1]
        Y2[Thread 2]
        Y3[Thread 3]
        Y4[Thread 4]
    end
    subgraph PostgresWorker["PostgresWorker (4 instances)"]
        P1[Thread 1]
        P2[Thread 2]
        P3[Thread 3]
        P4[Thread 4]
    end

    W1 -->|SymbolQueue| Y1 & Y2 & Y3 & Y4
    Y1 & Y2 & Y3 & Y4 -->|PostgresUploading| P1 & P2 & P3 & P4
    P1 & P2 & P3 & P4 --> DB[(Postgres: prices table)]
```

Each worker class is a `threading.Thread` that starts itself inside `__init__`. `YamlPipelineExecutor` is itself a `threading.Thread` (`reader.py`): its `run()` builds everything then polls worker liveness until the whole pipeline drains.

**Current limitation:** a queue can only be consumed by one worker stage. Queues fan work out across the *instances* of a single consuming worker (each item goes to exactly one instance), not across multiple different worker stages. A fanout/broadcast directive (send every item to all subscriber stages) vs. the current direct/round-robin behavior is a documented TODO in the YAML, not yet implemented.

## Poison-pill (DONE) propagation

The hard part: a producer stage doesn't know how many consumer *threads* are reading its output queue, so it can't hardcode how many `"DONE"` sentinels to send. `YamlPipelineExecutor.run()` solves this centrally instead of leaving it to each worker file.

```mermaid
sequenceDiagram
    participant R as YamlPipelineExecutor.run()
    participant WQ as SymbolQueue
    participant Y as YahooFinanceWorker x4
    participant PQ as PostgresUploading
    participant P as PostgresWorker x4

    Note over R: _initialize_workers() already ran:<br/>_queue_consumers[SymbolQueue] = 4<br/>_queue_consumers[PostgresUploading] = 4<br/>_downstream_queues[WikiWorker] = [SymbolQueue]<br/>_downstream_queues[YahooFinanceWorker] = [PostgresUploading]

    R->>R: poll: WikiWorker thread alive?
    Note over R: WikiWorker thread has finished (0 alive)
    loop 4 times (number_of_consumers)
        R->>WQ: put("DONE")
    end
    Y->>WQ: get() -> "DONE" (one each)
    Note over Y: each of the 4 threads exits on its own DONE

    R->>R: poll: any YahooFinanceWorker thread alive?
    Note over R: all 4 YahooFinanceWorker threads have finished (0 alive)
    loop 4 times (number_of_consumers)
        R->>PQ: put("DONE")
    end
    P->>PQ: get() -> "DONE" (one each)
    Note over P: each of the 4 threads exits on its own DONE<br/>PostgresWorker has no output_queues, so nothing further is signalled
```

For every worker, on the tick where *all* of its instances are dead, `run()` looks up `_downstream_queues[worker]` and, for each downstream queue, pushes `_queue_consumers[queue]` copies of `"DONE"` — exactly one per consumer thread. Each consumer (`YahooFinancePriceScheduler`, `PostgresMasterScheduler`) just exits on its own single `"DONE"`; it no longer forwards DONE itself. That decouples upstream/downstream instance counts, which the old per-worker-file approach didn't: it used to send one `"DONE"` per *queue* (not per consumer thread), so only 1 of N consumer threads got a real signal and the rest relied on falling through their 20s `queue.get(timeout=20)` `Empty` — not a hang, but not a clean shutdown either.
