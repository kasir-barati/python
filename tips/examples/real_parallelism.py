def pool_example():
    from math import factorial
    from multiprocessing import Pool
    from time import perf_counter

    def calc_factorial() -> list[int]:
        start = perf_counter()
        result = [factorial(num) for num in range(12_000)]
        end = perf_counter()
        print(end - start)
        return result

    def calc_factorial_in_a_pool() -> list[int]:
        start = perf_counter()
        with Pool(5) as process:
            result = process.map(factorial, range(12_000))
        end = perf_counter()
        print(end - start)
        return result

    result1 = calc_factorial()
    result2 = calc_factorial_in_a_pool()

    print(all(num1 == num2 for num1, num2 in zip(result1, result2)))


def process_example() -> None:
    from datetime import datetime
    from math import factorial
    from multiprocessing import Process
    from time import sleep

    def heartbeat(interval: int) -> None:
        while True:
            print(f"[{datetime.now().isoformat()}] running...")
            sleep(interval)

    heartbeat_process = Process(target=heartbeat, args=(5,), daemon=True)
    heartbeat_process.start()

    result = [factorial(num) for num in range(12_000)]

    print(f"First item: {result.copy().pop(0)}")


def queue_example() -> None:
    from multiprocessing import Process, Queue
    from random import sample
    from string import ascii_letters
    from time import sleep
    from typing import TypedDict
    from uuid import uuid4

    class User(TypedDict):
        id: str
        name: str

    def create_user(queue: "Queue[User]") -> None:
        name = "".join(sample(ascii_letters * 6, 6))
        queue.put({"id": str(uuid4()), "name": name})

    def user_created_listener(queue: "Queue[User | None]") -> None:
        while True:
            user = queue.get()

            if user is None:
                sleep(5)
                continue

            print(user)

    queue: "Queue[User]" = Queue()
    listener_process = Process(target=user_created_listener, args=(queue,))

    listener_process.start()

    create_user(queue)
    create_user(queue)

    listener_process.join()


def communication_channel_example() -> None:
    """
    In this example you can send data back and forth between the main process and spawned process.
    """

    from multiprocessing import Pipe, Process, connection
    from time import sleep

    def worker(connection: connection.Connection) -> None:
        for index in range(1, 5):
            connection.send(index**2)
            sleep(2)
        print("[worker] closing the connection...")
        connection.close()

    parent_connection, child_connection = Pipe()
    process = Process(target=worker, args=(child_connection,))
    process.start()

    # I do not want to send anything to the worker, so I can close the child_connection immediately.
    # But if you want to do it first you need to pass duplex=True arg when instantiating the Pipe and then also you should not close the child connection.
    child_connection.close()

    # Why I am not use child_connection.closed? Because when the worker closes child_connection, it only affects the worker's copy.
    while True:
        try:
            print("-" * 49)
            print("|\t[main process] waiting for new data\t|")
            print(f"|\t{parent_connection.recv() = }\t\t|")
            print(f"|\t{child_connection.closed  = }\t\t|")
            print("-" * 49)
            sleep(3)
        except EOFError:
            print("|\t[main process] received last message\t|")
            print("-" * 49)
            break

    process.join()


def locking_a_shared_state_between_processes() -> None:
    from multiprocessing import Lock, Process, Value
    from multiprocessing.sharedctypes import Synchronized
    from typing import Any

    # TODO: https://discuss.python.org/t/returntype-will-be-a-useful-utility-type/99371
    def worker(lock: Any, counter: "Synchronized[int]") -> None:
        for _ in range(100):
            with lock:
                counter.value += 1

    lock = Lock()
    # The first argument to Value() is a typecode (like 'i' for int, 'd' for double).
    # Learn more about typecodes: https://docs.python.org/3/library/array.html#module-array
    shared_counter: "Synchronized[int]" = Value("i", 0)

    processes = [Process(target=worker, args=(lock, shared_counter)) for _ in range(5)]

    [process.start() for process in processes]
    [process.join() for process in processes]

    print(f"{shared_counter.value = }")
