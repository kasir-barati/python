from threading import Thread
from time import sleep

done = False


def worker() -> None:
    global done
    counter = 0
    while not done:
        sleep(1)
        counter += 1
        print(f"{counter = }")


# We are not invoking the worker to block the main thread, but rather we are creating a thread and then Python invoke it in that thread when we say thread.start() which ain't gonna block the main thread.
thread = Thread(target=worker, daemon=True)
thread.start()


input("Press Enter to quit!\n")  # pyright: ignore[reportUnusedCallResult]
done = True
