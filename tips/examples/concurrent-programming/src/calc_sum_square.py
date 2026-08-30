from threading import Thread

def calculate_sum_square(n: int):
    sum_square = 0

    for i in range(n):
        sum_square += i ** 2

    print(f"{sum_square=}")

class SumSquareWorker(Thread):
    def __init__(self, n: int, **kwargs):
        super().__init__(**kwargs)
        self._n = n
        self.start()

    def _calc(self):
        calculate_sum_square(self.n)

    def run(self):
        self._calc()
