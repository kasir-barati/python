from threading import Thread
from time import sleep


class DummyWorker(Thread):
    def __init__(self, seconds: int, **kwargs):
        super().__init__(**kwargs)
        self._seconds = seconds
        self.run()

    def _dummy_work(self):
        sleep(self._seconds)

    def run(self):
        self._dummy_work()
