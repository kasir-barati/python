from typing import AsyncGenerator
import pytest
from testcontainers.rabbitmq import RabbitMqContainer
from tests.services.rabbitmq_service import RabbitmqService


@pytest.fixture(scope="function")
async def rabbitmq_container() -> AsyncGenerator[RabbitMqContainer, None]:
    """
    Session-scoped fixture that provides a RabbitMQ container for all tests.
    """
    container = RabbitMqContainer("rabbitmq:3.13.4-alpine")
    container.start()

    try:
        yield container
    finally:
        container.stop()


@pytest.fixture(scope="function")
async def rabbitmq_service(
    rabbitmq_container: RabbitMqContainer,
) -> AsyncGenerator[RabbitmqService, None]:
    """
    Function-scoped fixture that provides a RabbitMQ service instance.
    """
    host = rabbitmq_container.get_container_host_ip()
    port = rabbitmq_container.get_exposed_port(5672)
    user = rabbitmq_container.username
    password = rabbitmq_container.password
    connection_url = f"amqp://{user}:{password}@{host}:{port}/"
    service = RabbitmqService(connection_url)

    await service.connect()

    try:
        yield service
    finally:
        await service.disconnect()
