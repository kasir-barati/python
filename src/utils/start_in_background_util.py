import logging
from multiprocessing import Process
from types import FunctionType
from typing import Any

logger = logging.getLogger("uvicorn")
processes: list[Process] = []


def start_in_background(func: FunctionType):
    process = Process(target=func)
    process.start()
    processes.append(process)


def cleanup_background_processes(*_: Any):
    logger.info("cleaning up the background processes")

    for process in processes:
        if process.is_alive():
            process.terminate()

    [process.join() for process in processes]
