import time
import uuid
from collections.abc import Iterator
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from testcontainers.core.container import DockerContainer
from testcontainers.core.wait_strategies import LogMessageWaitStrategy

_ALEMBIC_INI = Path(__file__).resolve().parents[1] / "shared" / "alembic.ini"


@pytest.fixture(scope="session")
def rabbitmq_url() -> Iterator[str]:
    container = DockerContainer("rabbitmq:3.13-management-alpine")
    container.with_exposed_ports(5672)
    container.waiting_for(LogMessageWaitStrategy("Server startup complete"))
    with container:
        host = container.get_container_host_ip()
        port = container.get_exposed_port(5672)
        yield f"amqp://guest:guest@{host}:{port}/"


@pytest.fixture(scope="session")
def redis_url() -> Iterator[str]:
    container = DockerContainer("redis:7-alpine")
    container.with_exposed_ports(6379)
    container.waiting_for(LogMessageWaitStrategy("Ready to accept connections"))
    with container:
        host = container.get_container_host_ip()
        port = container.get_exposed_port(6379)
        yield f"redis://{host}:{port}/0"


def _wait_for_postgres(url: str, timeout: float = 30.0) -> None:
    # Postgres logs "ready to accept connections" twice during its startup
    # sequence (once before it restarts itself), so a log-based wait
    # strategy is unreliable here. Polling a real connection is not.
    deadline = time.monotonic() + timeout
    last_error: Exception | None = None
    while time.monotonic() < deadline:
        try:
            create_engine(url).connect().close()
            return
        except OperationalError as exc:
            last_error = exc
            time.sleep(0.5)
    raise TimeoutError(f"postgres not ready in time: {last_error}")


def _migrate(url: str) -> None:
    config = Config(str(_ALEMBIC_INI))
    config.set_main_option("sqlalchemy.url", url)
    command.upgrade(config, "head")


@pytest.fixture(scope="session")
def postgres_url() -> Iterator[str]:
    container = DockerContainer("postgres:16-alpine")
    container.with_exposed_ports(5432)
    container.with_env("POSTGRES_PASSWORD", "postgres")
    container.with_env("POSTGRES_DB", "app")
    with container:
        host = container.get_container_host_ip()
        port = container.get_exposed_port(5432)
        url = f"postgresql+psycopg://postgres:postgres@{host}:{port}/app"
        _wait_for_postgres(url)
        _migrate(url)
        yield url


@pytest.fixture
def queue_name() -> str:
    # Unique per test so the two tests don't see each other's messages on
    # the shared, session-scoped RabbitMQ container.
    return f"tasks-{uuid.uuid4().hex[:8]}"
