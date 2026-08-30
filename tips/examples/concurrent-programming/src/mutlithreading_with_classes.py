from time import time

from .calc_sum_square import SumSquareWorker
from .dummy import DummyWorker

def multithreading_with_classes():
    print("\n\r")
    print("=" * 20)
    print("Multithreading with classes & inheritance")
    start_time = time()

    calc_workers: list[SumSquareWorker] = []
    for i in range(1, 10):
        calc_args = i * 10_000_000
        sum_square_worker = SumSquareWorker(n=calc_args)
        calc_workers.append(sum_square_worker)
    for worker in calc_workers:
        worker.join()
    end_time = time.time()
    print(f"It took {round(end_time - start_time, 1)} seconds to finish")
    
    start_time = time()
    dummy_workers: list[DummyWorker] = []
    for i in range(1, 3):
        dummy_worker = DummyWorker(seconds=i)
        dummy_workers.append(dummy_worker)
    for worker in dummy_workers:
        worker.join()
    end_time = time()
    print(f"Dummy process finished in {round(end_time - start_time, 1)}")

    print("=" * 20)
    print("\n\r")