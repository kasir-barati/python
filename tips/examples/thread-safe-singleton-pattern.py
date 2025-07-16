import os
import threading
from typing import Any

from .retry import retry


class SingletonMeta(type):
    _instances: dict[Any, Any] = {}
    _lock: threading.Lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class AccessTokenSingleton(metaclass=SingletonMeta):
    __timer: threading.Timer | None = None

    def __init__(self) -> None:
        self.__refresh_interval = int(
            os.getenv("ACCESS_TOKEN_REFRESH_RATE_IN_SECONDS", 10_000)
        )  # Pick a number which gives your app a little bit room to fetch the new token before getting too close to expiration date
        self.__refresh_lock = threading.Lock()
        self.__access_token = self.__fetch_access_token()
        self.__schedule_refresh()

    def __fetch_access_token(self) -> str:
        """
        Fetches a JWT token from the XYZ API

        TODO Fetch the token from the API
        """
        return "some.jwt.token"

    def __refresh_access_token(self):
        retry_times = 3
        try:
            new_token = retry(self.__fetch_access_token, retry_times, backoff=2)
        except Exception as e:
            print(f"Failed to fetch the token after {retry_times} times: {e}")
            new_token = None

        if new_token is None:
            return

        with self.__refresh_lock:
            self.__access_token = new_token

        self.__schedule_refresh()

    def __schedule_refresh(self):
        """
        Schedules fetching access_token and replacing it with the existing one
        """
        self.__timer = threading.Timer(
            self.__refresh_interval, self.__refresh_access_token
        )
        self.__timer.daemon = True  # Allows program to exit cleanly
        self.__timer.start()

    def get_access_token(self):
        """
        Returns the JWT token
        """

        with self.__refresh_lock:
            return self.__access_token
