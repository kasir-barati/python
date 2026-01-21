import asyncio
import signal
from functools import lru_cache

from common.config import Settings
from common.logger import get_logger
from common.rabbitmq_handler import RabbitmqHandler, RabbitmqHeaders
from constants.events import (
    BATCH_SIZE,
    EXCHANGE_NAME,
    EXCHANGE_TYPE,
    QUEUE_NAME,
    ROUTING_KEY,
)
from interfaces.message import GreetMessage


@lru_cache()
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]


settings = get_settings()
logger = get_logger(__name__)


def process_message(message: GreetMessage, headers: RabbitmqHeaders) -> None:
    correlation_id = headers.get("correlation-id")
    try:
        logger.info(
            f"📨 Processing message: {message['message']}",
            extra={"correlation_id": correlation_id},
        )
    except Exception as e:
        logger.error(
            f"Error processing message: {e}", extra={"correlation_id": correlation_id}
        )
        raise


async def main():
    logger.info("Starting RabbitMQ Consumer Application")
    logger.info(
        f"Configuration: Exchange={EXCHANGE_NAME}, Queue={QUEUE_NAME}, "
        f"RoutingKey={ROUTING_KEY}, BatchSize={BATCH_SIZE}, "
        f"PrefetchCount={settings.rabbitmq.prefetch_count}"
    )

    handler = RabbitmqHandler(
        callback=process_message,
        exchange_name=EXCHANGE_NAME,
        exchange_type=EXCHANGE_TYPE,
        queue_name=QUEUE_NAME,
        routing_key=ROUTING_KEY,
    )

    # Setup graceful shutdown
    loop = asyncio.get_event_loop()

    def signal_handler():
        logger.info("Received shutdown signal")
        asyncio.create_task(handler.close())
        loop.stop()

    # Register signal handlers
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, signal_handler)

    try:
        await handler.connect()
        await handler.start_consuming()
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt")
    except Exception as e:
        logger.error(f"Application error: {e}")
        raise
    finally:
        await handler.close()
        logger.info("Application shutdown complete")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Application terminated by user")
