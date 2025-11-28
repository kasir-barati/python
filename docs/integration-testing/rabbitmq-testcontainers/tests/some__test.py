import asyncio
import io
from contextlib import redirect_stdout
from pytest import MonkeyPatch
from tests.services.rabbitmq_service import RabbitmqService


class TestRabbitMQIntegration:
    async def test_publish_and_consume_single_message(
        self, rabbitmq_service: RabbitmqService, monkeypatch: MonkeyPatch
    ):
        exchange = await rabbitmq_service.declare_exchange("test_exchange", "direct")
        queue = await rabbitmq_service.declare_queue("test_queue")
        await rabbitmq_service.bind_queue(queue, exchange, "test_routing_key")
        await rabbitmq_service.publish_message(
            "test_exchange", "test_routing_key", "test_queue"
        )
        monkeypatch.setenv("RABBITMQ_URL", rabbitmq_service.connection_url)
        monkeypatch.setenv("ENV", "test")
        captured_output = io.StringIO()
        from src.main import main

        with redirect_stdout(captured_output):
            try:
                # Run main() with a timeout - it will process the message and then timeout
                await asyncio.wait_for(main(), timeout=3.0)
            except asyncio.TimeoutError:
                pass

        output = captured_output.getvalue().strip()
        assert "test_queue" in output, f"Expected 'test_queue' in output, got: {output}"
