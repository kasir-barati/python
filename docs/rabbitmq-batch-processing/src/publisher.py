"""Dummy publisher script for testing"""

import argparse
import asyncio
import json
import uuid
from datetime import datetime
from functools import lru_cache

from aio_pika import ExchangeType, Message, connect_robust
from src.constants.events import EXCHANGE_NAME, ROUTING_KEY

from common.config import Settings
from common.logger import get_logger
from interfaces.message import GreetMessage


@lru_cache()
def get_settings() -> Settings:
    """Retrieve application settings"""
    return Settings()  # type: ignore[call-arg]


settings = get_settings()
logger = get_logger(__name__)


async def publish_messages(num_messages: int = 20) -> None:
    """
    Publish test messages to RabbitMQ

    Args:
        num_messages: Number of messages to publish
    """
    try:
        # Connect to RabbitMQ
        logger.info(
            f"Connecting to RabbitMQ at {settings.rabbitmq.host}:{settings.rabbitmq.port}"
        )
        connection = await connect_robust(settings.rabbitmq.url)
        channel = await connection.channel()

        # Declare exchange
        exchange = await channel.declare_exchange(
            name=EXCHANGE_NAME, type=ExchangeType.TOPIC, durable=True
        )
        logger.info(f"Connected to exchange: {EXCHANGE_NAME}")

        # Publish messages
        logger.info(f"Publishing {num_messages} messages...")
        for i in range(1, num_messages + 1):
            timestamp = datetime.now().isoformat()
            message_body: GreetMessage = {"message": f"Hi #{i} - {timestamp}"}

            message = Message(
                body=json.dumps(message_body).encode("utf-8"),
                content_type="application/json",
                delivery_mode=2,  # Persistent message
                headers={
                    "correlation-id": str(uuid.uuid4()),
                },
            )

            # Extract routing key without wildcard for publishing
            routing_key = ROUTING_KEY.replace("#", "test").replace("*", "test")
            if routing_key.endswith("."):
                routing_key = routing_key + "test"

            await exchange.publish(message=message, routing_key=routing_key)

            logger.info(f"✅ Published message {i}/{num_messages}: {message_body}")

            # Small delay between messages
            await asyncio.sleep(0.1)

        logger.info(f"Successfully published {num_messages} messages")

        # Close connection
        await connection.close()
        logger.info("Connection closed")

    except Exception as e:
        logger.error(f"Error publishing messages: {e}")
        raise


def main():
    """Main entry point for publisher script"""
    parser = argparse.ArgumentParser(description="Publish test messages to RabbitMQ")
    parser.add_argument(
        "-n",
        "--num-messages",
        type=int,
        default=20,
        help="Number of messages to publish (default: 20)",
    )

    args = parser.parse_args()

    logger.info("Starting RabbitMQ Publisher")
    logger.info(f"Configuration: Exchange={EXCHANGE_NAME}, RoutingKey={ROUTING_KEY}")

    try:
        asyncio.run(publish_messages(args.num_messages))
    except KeyboardInterrupt:
        logger.info("Publisher interrupted by user")
    except Exception as e:
        logger.error(f"Publisher failed: {e}")
        raise


if __name__ == "__main__":
    main()
