"""Logger factory"""

import logging
import sys
from functools import lru_cache
from typing import Any, MutableMapping, Protocol, TypedDict

from pythonjsonlogger import jsonlogger

from common.config import Settings


@lru_cache()
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]


class LogExtra(TypedDict, total=False):
    correlation_id: str | None


class TypedLogger(Protocol):
    def debug(
        self,
        msg: str,
        *,
        extra: LogExtra | None = None,
        stack_info: bool = False,
        **kwargs: Any,
    ) -> None: ...
    def info(
        self,
        msg: str,
        *,
        extra: LogExtra | None = None,
        stack_info: bool = False,
        **kwargs: Any,
    ) -> None: ...
    def warning(
        self,
        msg: str,
        *,
        extra: LogExtra | None = None,
        stack_info: bool = False,
        **kwargs: Any,
    ) -> None: ...
    def error(
        self,
        msg: str,
        *,
        extra: LogExtra | None = None,
        stack_info: bool = False,
        **kwargs: Any,
    ) -> None: ...
    def critical(
        self,
        msg: str,
        *,
        extra: LogExtra | None = None,
        stack_info: bool = False,
        **kwargs: Any,
    ) -> None: ...


class CorrelationIdAdapter(logging.LoggerAdapter):
    def process(
        self, msg: str, kwargs: MutableMapping[str, Any]
    ) -> tuple[str, MutableMapping[str, Any]]:
        extra = kwargs.get("extra")

        if extra and "correlation_id" in extra:
            correlation_id = extra["correlation_id"]

            if not isinstance(
                self.logger.handlers[0].formatter, jsonlogger.JsonFormatter
            ):
                msg = f"[correlation_id={correlation_id}] {msg}"

        return msg, kwargs


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    @staticmethod
    def __snake_to_camel(snake_str: str) -> str:
        components = snake_str.split("_")
        first_component = components[0]
        capitalized_rest = "".join(x.title() for x in components[1:])  # SomeExample

        return first_component + capitalized_rest

    def add_fields(
        self,
        log_record: dict[str, Any],
        record: logging.LogRecord,
        message_dict: dict[str, Any],
    ) -> None:
        super().add_fields(log_record, record, message_dict)

        if (
            hasattr(record, "correlation_id")
            and getattr(record, "correlation_id", None) is not None
        ):
            log_record["correlation_id"] = getattr(record, "correlation_id")
        elif "correlation_id" in log_record:
            # Remove correlation_id if it's None or doesn't exist
            del log_record["correlation_id"]

        keys_to_convert = list(log_record.keys())
        for key in keys_to_convert:
            if "_" in key:
                camel_key = self.__snake_to_camel(key)
                log_record[camel_key] = log_record.pop(key)


def get_logger(name: str) -> TypedLogger:
    settings = get_settings()
    logger = logging.getLogger(name)

    logger.setLevel(settings.logger.log_level)
    logger.propagate = False
    logger.handlers.clear()

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(settings.logger.log_level)

    if settings.logger.json_logging:
        formatter = CustomJsonFormatter(
            "%(asctime)s %(levelname)s %(name)s %(message)s",
            rename_fields={"levelname": "level", "asctime": "timestamp"},
        )
    else:
        formatter = logging.Formatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return CorrelationIdAdapter(logger, {})
