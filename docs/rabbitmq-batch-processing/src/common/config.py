"""Configuration settings"""

from logging import getLevelName, getLevelNamesMapping

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


LogLevel = list(getLevelNamesMapping().keys())


class Rabbitmq(BaseSettings):
    host: str = Field(default="localhost")
    port: int = Field(default=5672)
    user: str = Field(default="guest")
    password: str = Field(default="guest")
    vhost: str = Field(default="/")
    prefetch_count: int = Field(default=10, ge=1, le=100)
    max_workers: int = Field(
        default=4, description="Number of threads for parallel batch processing"
    )

    @property
    def url(self) -> str:
        return (
            f"amqp://{self.user}:{self.password}@{self.host}:{self.port}/{self.vhost}"
        )


class Logger(BaseSettings):
    plain_log_level: str = Field(default="INFO", alias="log_level")
    json_logging: bool = Field(default=False)

    @field_validator("plain_log_level")
    @classmethod
    def validate_level(cls, level: str):
        if level.upper() not in LogLevel:
            raise ValueError(f"Invalid log level: {level}, must be one of {LogLevel}")

        return level

    @property
    def log_level(self) -> int:
        return getLevelName(self.plain_log_level.upper())


class Settings(BaseSettings):
    rabbitmq: Rabbitmq
    logger: Logger

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        str_strip_whitespace=True,
        case_sensitive=False,
        extra="ignore",
    )


if __name__ == "__main__":
    settings = Settings()
    print(settings.model_dump())
