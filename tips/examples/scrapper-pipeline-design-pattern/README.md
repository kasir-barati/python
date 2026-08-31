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

## Queue modes: direct vs. fanout

A queue in the `queues:` section takes an optional `mode`, defaulting to `direct`:

```yaml
queues:
  - name: SymbolQueue
    mode: direct    # default — one consuming stage, work split across its instances
  - name: PostProcessing
    mode: fanout     # every subscribing stage gets every item
```

- **`direct`** (default): a queue may be declared as `input_queue` by exactly one worker stage. That stage's *instances* still compete for items round-robin. Declaring the same `direct` queue as `input_queue` on a second stage is a load-time error — items would otherwise be silently split between the two stages instead of each getting the full stream.
- **`fanout`**: multiple stages may declare the same queue as `input_queue`. Under the hood `YamlPipelineExecutor` gives each subscribing stage its own physical queue and expands the producer's `output_queues` to write into all of them, so every subscriber sees every item; worker code is unchanged and stays unaware fan-out is even happening. Instances within one subscribing stage still compete over that stage's own copy.

```mermaid
flowchart LR
    subgraph direct["mode: direct"]
        DP[Producer] -->|SymbolQueue| DC1[MarketSentimentSkill instance 1]
        DP -->|SymbolQueue| DC2[MarketSentimentSkill instance 2]

        DC1 -->|SentimentQueue| SG[StrategyGeneratorSkill instance 1]
        DC2 -->|SentimentQueue| SG[StrategyGeneratorSkill instance 2]

        SG -->|TradingStrategyQueue| Output[NotificationService]
    end

    Note1["Auto-scales based on load"] -.- Output
```

```mermaid
flowchart LR
    subgraph fanout["mode: fanout"]
        FP[Producer] -->|PostProcessing copy A| FA1[MarketSentimentSkill instance 1]
        FP -->|PostProcessing copy A| FA2[MarketSentimentSkill instance 2]
        FP -->|PostProcessing copy B| FB1[ExplainabilitySkill instance 1]
    end
```

In `direct` mode each item goes to exactly one stage instance, chosen by whichever instance happens to `get()` it first. In `fanout` mode every subscribing *stage* gets its own copy of every item; only the choice of *which instance within that stage* handles it is round-robin.

## Combining modes in one pipeline

A single pipeline can mix both: fan out to several skills, then chain some of those skills serially. `mode` is set per queue, so each queue in the pipeline picks whichever fits its own consumers.

```mermaid
flowchart LR
    Producer -->|PostProcessing<br/>mode: fanout| MarketSentimentSkill
    Producer -->|PostProcessing<br/>mode: fanout| ExplainabilitySkill

    subgraph MarketSentimentSkill["MarketSentimentSkill (2 instances)"]
        MS1[instance 1]
        MS2[instance 2]
    end
    subgraph ExplainabilitySkill["ExplainabilitySkill (1 instance)"]
        E1[instance 1]
    end
    subgraph StrategyGeneratorSkill["StrategyGeneratorSkill (2 instances)"]
        SG1[instance 1]
        SG2[instance 2]
    end

    MS1 & MS2 -->|SentimentQueue<br/>mode: direct| SG1 & SG2
    SG1 & SG2 -->|TradingStrategyQueue<br/>mode: direct| NotificationService
```

```yaml
queues:
  - name: PostProcessing
    description: Symbols to analyze, broadcast to every downstream skill
    mode: fanout
  - name: SentimentQueue
    description: Market sentiment results, feeds strategy generation
  - name: TradingStrategyQueue
    description: Generated trading strategies, feeds notifications

workers:
  - name: Producer
    location: workers.producer
    class: ProducerScheduler
    instances: 1
    output_queues:
      - PostProcessing

  - name: MarketSentimentSkill
    location: workers.market_sentiment
    class: MarketSentimentScheduler
    instances: 2
    input_queue: PostProcessing
    output_queues:
      - SentimentQueue

  - name: ExplainabilitySkill
    location: workers.explainability
    class: ExplainabilityScheduler
    instances: 1
    input_queue: PostProcessing

  - name: StrategyGeneratorSkill
    location: workers.strategy_generator
    class: StrategyGeneratorScheduler
    instances: 2
    input_queue: SentimentQueue
    output_queues:
      - TradingStrategyQueue

  - name: NotificationService
    location: workers.notification
    class: NotificationScheduler
    instances: 1
    input_queue: TradingStrategyQueue
```

`PostProcessing` needs `mode: fanout` since two stages (`MarketSentimentSkill`, `ExplainabilitySkill`) both declare it as `input_queue`. `SentimentQueue` and `TradingStrategyQueue` stay `direct` (the default) since each has exactly one subscribing stage — that stage's `instances` still compete round-robin for items, same as `WikiWorker` -> `SymbolQueue` above. No YAML reader changes are needed for this; `mode` is already read per-queue.

## Poison-pill (DONE) propagation

The hard part: a producer stage doesn't know how many consumer *threads* are reading its output queue, so it can't hardcode how many `"DONE"` sentinels to send. `YamlPipelineExecutor.run()` solves this centrally instead of leaving it to each worker file.

```mermaid
sequenceDiagram
    participant R as YamlPipelineExecutor.run()
    participant WQ as SymbolQueue
    participant Y as YahooFinanceWorker x4
    participant PQ as PostgresUploading
    participant P as PostgresWorker x4

    Note over R: _initialize_workers() already ran:<br/>_queue_consumers[SymbolQueue] = [(YahooFinanceWorker's queue, 4)]<br/>_queue_consumers[PostgresUploading] = [(PostgresWorker's queue, 4)]<br/>_downstream_queues[WikiWorker] = [SymbolQueue]<br/>_downstream_queues[YahooFinanceWorker] = [PostgresUploading]

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

For every worker, on the tick where *all* of its instances are dead, `run()` looks up `_downstream_queues[worker]` and, for each downstream queue name, iterates every `(physical queue, instance count)` pair in `_queue_consumers[queue]` — one pair per subscribing stage — pushing that many copies of `"DONE"` into that stage's own queue. Each consumer (`YahooFinancePriceScheduler`, `PostgresMasterScheduler`) just exits on its own single `"DONE"`; it no longer forwards DONE itself. That decouples upstream/downstream instance counts, which the old per-worker-file approach didn't: it used to send one `"DONE"` per *queue* (not per consumer thread), so only 1 of N consumer threads got a real signal and the rest relied on falling through their 20s `queue.get(timeout=20)` `Empty` — not a hang, but not a clean shutdown either.

In `fanout` mode this same loop naturally scales: each subscribing stage has its own `(queue, instance count)` entry, so a stage with 2 instances gets 2 `"DONE"`s in its own queue and a stage with 1 instance gets 1, regardless of how many other stages are also fanned out to.
