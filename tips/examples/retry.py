from time import sleep
from typing import Callable, TypeVar

TResult = TypeVar("TResult")


def retry(
    func: Callable[[], TResult],
    times: int,
    *,
    exceptions: type[BaseException] | tuple[type[BaseException], ...] = Exception,
    delay: int = 0,
    backoff: int = 1,
) -> TResult | None:
    """
    Try calling `func()` up to `times` attempts.
    If it succeeds, return its result.
    If it raises `exceptions`, wait (optionally) then retry.
    After exhausting attempts returns None.
    """
    current_delay = delay
    for attempt in range(1, times + 1):
        try:
            return func()
        except exceptions as e:
            if attempt == times:
                return None
            if delay > 0:
                sleep(current_delay)
                current_delay *= backoff
    return None
