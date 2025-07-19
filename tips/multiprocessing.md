# Multiprocessing

- [Examples](./examples/real_parallelism.py).
- When you have multiprocessing you sometimes need to lock something in order to prevent simultaneous access. For this look at the `locking_a_shared_state_between_processes` function. This can be quite useful when you wanna go for refreshing your access token in a JWT setup ([what is refresh token](https://auth0.com/blog/refresh-tokens-what-are-they-and-when-to-use-them/)).

> [!TIP]
>
> We also have `Semaphore` which enables your processes to access same resource simultaneously, and how many processes can access the resource is configurable:
>
> ```py
> import random
> from multiprocessing import Process, Semaphore
> from time import sleep
> from typing import Any
>
>
> def worker(semaphore: Any, index: int) -> None:
>     with semaphore:
>         print(f"Process {index}# accessed some resource.")
>         sleep(random.uniform(1, 3))
>     print(f"\tProcess {index}# has been completed")
>
>
> if __name__ == "__main__":
>     semaphore = Semaphore(2)
>
>     processes = [Process(target=worker, args=(semaphore, index)) for index in range(6)]
>
>     [process.start() for process in processes]
>     [process.join() for process in processes]
> ```

## `Queue`

- **Hot tip**: if you try to use generic type annotation you will get an error at runtime:

  ```cmd
  Traceback (most recent call last):
  File "/home/kasir/projects/python/tips/examples/real_parallelism.py", line 81, in <module>
    queue_example()
  File "/home/kasir/projects/python/tips/examples/real_parallelism.py", line 61, in queue_example
    def create_user(queue: Queue[User]) -> None:
                           ~~~~~^^^^^^
  TypeError: 'method' object is not subscriptable
  ```

  To fix this you can use string annotation in Python.
