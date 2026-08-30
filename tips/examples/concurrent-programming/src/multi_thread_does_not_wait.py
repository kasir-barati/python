import time
from threading import Thread

from .calc_sum_square import calculate_sum_square


def creates_multiple_threads_does_not_wait_for_them():
    """
    Pass by object reference: every variable is a reference, and those references get copied by value on assignment/append/argument-passing.

    - thread = Thread(...) creates a Thread object somewhere in memory, and the local variable thread is a reference (a pointer, conceptually) to that object.
    - concurrent_threads.append(thread) copies that reference into the list — the list now holds a pointer to the same object thread points to. The list doesn't care what thread does afterward.
    - On the next loop iteration, thread = Thread(...) doesn't mutate the old object — it creates a brand new Thread object and rebinds the name thread to point at that new one. The old object is untouched; it still exists (kept alive by the list's reference to it), just no longer reachable via the name thread.

    IMPORTANT: when a loop variable is captured by closure inside a function/lambda that runs later, e.g.
    ```py
    for i in range(...):
        Thread(target=lambda: print(i))
    ```
    All threads would then see whatever i ended up being, because closures capture the variable, not its value at creation time. to offset that you must write:
    ```py
    for i in range(...):
        Thread(target=lambda args=i: print(args))
    ```
    Here `args=i` is evaluated immediately when the lambda object is created, capturing that iteration's `i` value into the lambda's own default, independent of what the loop variable does afterward.
    Or event better would be sidestepping closures entirely by passing values through Thread's `args=` parameter instead of a lambda:
    ```py
    for i in range(...):
        Thread(target=some_func, args=(i,))
    ```
    """
    print("\n\r")
    print("=" * 20)
    print("It is NOT gonna wait for the threads to finish, once they are registered!")

    start_time = time.time()

    for i in range(1, 10):
        calc_args = i * 10_000_000
        # Args must be a tuple.
        # So instead of invoking calculate_sum_square it is passing it to a thread and invokes it there with the args we passed to it.
        thread = Thread(target=calculate_sum_square, args=(calc_args, ))
        # You MUST start it first.
        thread.start()

    end_time = time.time()

    print(f"NOW YOU CAN SEE IT WON'T wait: {round(end_time - start_time, 1)}")
    print("The timer is also executed in the main thread and it's NOT creating new threads...")

    start_time = time.time()

    for i in range(1, 2):
        time.sleep(i * 10)

    end_time = time.time()

    print(f"Finished dummy sleeps in: {round(end_time - start_time, 1)}")
    print("=" * 20)
    print("\n\r")