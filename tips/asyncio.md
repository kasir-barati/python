# AsyncIO

> [!IMPORTANT]
>
> We can only have **one running event loop per thread** and by default, we're only going to be running this on one core and one single thread. So basically what that means is we're only going to have one `asyncio.run` call, which is going to be the entry point to our program:
>
> ```py
> import asyncio
> async def dummy_async():
>     await asyncio.sleep(123)
> if __name__ == "__main__":
>     asyncio.run(dummy_async())
> ```

In Python if you push too many tasks into event loop some of them might timeout before Python gets to execute them! If that happened to you you might wanna start batching them and push more tasks into the event loop more moderately. And if you are already batching them, maybe reduce the batch sizes. 

```py
import asyncio
import time


async def worker(task_id, semaphore):
    created = time.monotonic()

    # Give every task only 0.5 seconds from creation.
    deadline = created + 0.5

    async with semaphore:
        started = time.monotonic()

        # How long did we wait before getting a chance to run?
        queue_time = started - created

        print(
            f"Task {task_id:02d} STARTED "
            f"(waited {queue_time:.3f}s)"
        )

        # Simulate actual work.
        await asyncio.sleep(1)

        print(f"Task {task_id:02d} FINISHED")


async def run_with_timeout(task_id, semaphore):
    try:
        # IMPORTANT:
        # The timeout starts when this coroutine is scheduled,
        # not when it finally acquires the semaphore.
        await asyncio.wait_for(
            worker(task_id, semaphore),
            timeout=0.5,
        )

    except asyncio.TimeoutError:
        elapsed = time.monotonic() - start_time

        print(
            f"Task {task_id:02d} ❌ TIMEOUT "
            f"({elapsed:.3f}s after creation)"
        )


async def main():
    global start_time
    start_time = time.monotonic()

    # Only 2 tasks can actually execute at once.
    semaphore = asyncio.Semaphore(2)

    # But we create 10 tasks immediately.
    tasks = [
        asyncio.create_task(
            run_with_timeout(i, semaphore)
        )
        for i in range(10)
    ]

    await asyncio.gather(*tasks)
asyncio.run(main())
```

Note that here we are forcing the timeout kinda by limiting how many semaphores the event loop can have. But if you'd like to see a visualization of it:

```mermaid
flowchart TD
    A["Create 10 asyncio tasks"] --> B["Task 0"]
    A --> C["Task 1"]
    A --> D["Task 2"]
    A --> E["Task 3"]
    A --> F["Task 4 ... 9"]

    B --> G{"Semaphore<br/>2 slots available"}
    C --> G

    G --> H["Task 0 & Task 1<br/>START"]
    H --> I["Do work<br/>~0.2 seconds"]
    I --> J["FINISHED"]

    D --> K["Waiting for semaphore"]
    E --> K
    F --> K

    K --> L{"0.5 second<br/>timeout reached?"}

    L -->|Yes| M["❌ TIMEOUT"]
    L -->|No| N["Acquire semaphore"]
    N --> O["START"]
```

And here's the timeline, which I think makes the phenomenon even clearer:

```mermaid
sequenceDiagram
    participant E as Event Loop
    participant T0 as Task 0
    participant T1 as Task 1
    participant T2 as Task 2
    participant T3 as Task 3

    Note over E: Create 10 tasks

    E->>T0: Start
    E->>T1: Start

    Note over T0,T1: Semaphore has only 2 slots

    T2-->>E: Waiting for semaphore
    T3-->>E: Waiting for semaphore

    Note over T2,T3: Still waiting...

    T0->>E: Work complete
    T1->>E: Work complete

    E->>T2: Acquire semaphore
    E->>T3: Acquire semaphore

    Note over T2,T3: If 0.5s deadline<br/>already passed...

    T2-->>E: ❌ Timeout
    T3-->>E: ❌ Timeout
```

> [!TIP]
>
> To overcome the limitation of one event loop per process you can of course as you might have guessed it create multiple processes and in each hen start an event loop.