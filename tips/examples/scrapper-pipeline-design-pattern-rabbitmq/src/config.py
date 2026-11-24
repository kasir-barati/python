"""Config as a service: the single place every worker reads its settings from."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import quote

from dotenv import load_dotenv

load_dotenv()

PIPELINE_YAML = Path(__file__).parent / "pipelines" / "wiki_yahoo_scraper_pipeline.yaml"


@dataclass(frozen=True)
class Config:
    rabbitmq_host: str = field(default_factory=lambda: os.environ.get("RABBITMQ_HOST", "localhost"))
    rabbitmq_port: int = field(default_factory=lambda: int(os.environ.get("RABBITMQ_PORT", "5672")))
    rabbitmq_user: str = field(default_factory=lambda: os.environ.get("RABBITMQ_USER", "guest"))
    rabbitmq_password: str = field(default_factory=lambda: os.environ.get("RABBITMQ_PASSWORD", "guest"))
    rabbitmq_vhost: str = field(default_factory=lambda: os.environ.get("RABBITMQ_VHOST", "/"))

    postgres_user: str = field(default_factory=lambda: os.environ.get("POSTGRES_USER", ""))
    postgres_password: str = field(default_factory=lambda: os.environ.get("POSTGRES_PASSWORD", ""))
    postgres_host: str = field(default_factory=lambda: os.environ.get("PG_HOST", "localhost"))
    postgres_port: str = field(default_factory=lambda: os.environ.get("POSTGRES_PORT", "5432"))
    postgres_db: str = field(default_factory=lambda: os.environ.get("POSTGRES_DB", "postgres"))

    @property
    def rabbitmq_url(self) -> str:
        return (
            f"amqp://{self.rabbitmq_user}:{self.rabbitmq_password}"
            f"@{self.rabbitmq_host}:{self.rabbitmq_port}/{quote(self.rabbitmq_vhost, safe='')}"
        )

    @property
    def postgres_url(self) -> str:
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


config = Config()
