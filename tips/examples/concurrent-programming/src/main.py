from .multi_thread_does_not_wait import creates_multiple_threads_does_not_wait_for_them
from .multi_thread_does_wait_for_calc import creates_multiple_threads_does_wait_for_calc
from .mutlithreading_with_classes import multithreading_with_classes


if __name__ == "__main__":
    creates_multiple_threads_does_not_wait_for_them()
    creates_multiple_threads_does_wait_for_calc()
    multithreading_with_classes()
