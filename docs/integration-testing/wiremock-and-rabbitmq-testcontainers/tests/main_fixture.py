from typing import AsyncGenerator
import pytest_asyncio
from testcontainers.rabbitmq import RabbitMqContainer
from testcontainers.core.container import DockerContainer
from tests.services.rabbitmq_service import RabbitmqService
from tests.services.payment_service import PaymentService
import time
import httpx


@pytest_asyncio.fixture(scope="function")
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


@pytest_asyncio.fixture(scope="function")
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


@pytest_asyncio.fixture(scope="function")
async def auth_service_container() -> AsyncGenerator[str, None]:
    """
    Function-scoped fixture that provides a WireMock container for mocking Auth Service.
    Returns the base URL of the WireMock server.
    """
    # Create WireMock container
    container = (
        DockerContainer("wiremock/wiremock:3.9.1")
        .with_exposed_ports(8080)
        .with_command("--global-response-templating --verbose")
    )

    container.start()

    try:
        # Get the exposed port and host
        wiremock_port = container.get_exposed_port(8080)
        wiremock_host = container.get_container_host_ip()
        base_url = f"http://{wiremock_host}:{wiremock_port}"

        # Wait for WireMock to be ready
        async with httpx.AsyncClient() as client:
            for _ in range(30):  # Wait up to 30 seconds
                try:
                    response = await client.get(f"{base_url}/__admin/health")
                    if response.status_code == 200:
                        break
                except:
                    pass
                time.sleep(1)
            else:
                raise RuntimeError("WireMock container failed to start")

        yield base_url

    finally:
        container.stop()


@pytest_asyncio.fixture(scope="function")
async def auth_service(
    auth_service_container: str,
) -> AsyncGenerator[PaymentService, None]:
    """
    Function-scoped fixture that provides a configured WireMock service.
    """
    service = PaymentService(auth_service_container)

    await service.reset()
    await service.mock_callback_api()

    try:
        yield service
    finally:
        await service.close()
