import time
from threading import Thread

from .calc_sum_square import calculate_sum_square


def creates_multiple_threads_does_wait_for_calc():
    print("\n\r")
    print("=" * 20)
    print("It is gonna wait for the threads to finish, once they are registered!")

    calc_start_time = time.time()
    calc_concurrent_threads: list[Thread] = []

    for i in range(1, 10):
        calc_args = i * 10_000_000
        # Args must be a tuple.
        # So instead of invoking calculate_sum_square it is passing it to a thread and invokes it there with the args we passed to it.
        thread = Thread(target=calculate_sum_square, args=(calc_args, ))
        # You MUST start it first.
        thread.start()
        calc_concurrent_threads.append(thread)

    for thread in calc_concurrent_threads:
        thread.join()

    calc_end_time = time.time()

    print(f"NOW YOU CAN SEE IT WON'T wait: {round(calc_end_time - calc_start_time, 1)}")
    print("Each timer is now executed in a separated threads, but just for you to see both patterns I am not waiting for them to finish here!")

    dummy_sleep_start_time = time.time()

    for i in range(1, 2):
        sleep_args = i * 10
        thread = Thread(target=time.sleep, args=(sleep_args, ))
        thread.start()

    dummy_sleep_end_time = time.time()

    print(f"NOW YOU CAN SEE IT WON'T wait: {round(dummy_sleep_end_time - dummy_sleep_start_time, 1)}")
    print("=" * 20)
    print("\n\r")