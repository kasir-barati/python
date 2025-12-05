import asyncio
import json
import pytest
from tests.services.payment_service import PaymentService
from tests.services.rabbitmq_service import RabbitmqService


class TestRabbitMQIntegration:
    @pytest.mark.asyncio
    async def test_publish_and_consume_single_message(
        self,
        rabbitmq_service: RabbitmqService,
        payment_service: PaymentService,
        monkeypatch: pytest.MonkeyPatch,
    ):
        exchange = await rabbitmq_service.declare_exchange("test_exchange", "direct")
        queue = await rabbitmq_service.declare_queue("test_queue")
        await rabbitmq_service.bind_queue(queue, exchange, "test_routing_key")
        await rabbitmq_service.publish_message(
            "test_exchange",
            "test_routing_key",
            {
                "name": "Integration Test",
                "callbackUrl": f"{payment_service.base_url}{payment_service.path_prefix}/callback",
            },
        )
        monkeypatch.setenv("RABBITMQ_URL", rabbitmq_service.connection_url)
        monkeypatch.setenv("ENV", "test")
        from src.main import main

        try:
            # Run main() with a timeout - it will process the message and then timeout
            await asyncio.wait_for(main(), timeout=3.0)
        except asyncio.TimeoutError:
            pass

        callback_calls = await payment_service.get_callback_requests()
        assert (
            json.loads(callback_calls[0].get("request").get("body")).get("message")
            == "Hi Integration Test"
        )
        assert (
            json.loads(callback_calls[0].get("response").get("body")).get("message")
            == "Payment processed successfully"
        )
