"""RabbitMQ Handler"""

import asyncio
import json
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
from typing import Any, Callable, List, TypedDict, cast

from aio_pika import ExchangeType, connect_robust
from aio_pika.abc import (
    AbstractChannel,
    AbstractIncomingMessage,
    AbstractQueue,
    AbstractRobustConnection,
)

from common.logger import get_logger

from .config import Settings


@lru_cache()
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]


settings = get_settings()
logger = get_logger(__name__)


RabbitmqHeaders = TypedDict("RabbitmqHeaders", {"correlation-id": str | None})


class RabbitmqHandler:
    """Handler for RabbitMQ message consumption"""

    def __init__(
        self,
        callback: Callable[[dict[str, Any], RabbitmqHeaders], None],
        exchange_name: str,
        exchange_type: str,
        queue_name: str,
        routing_key: str,
    ):
        self.__callback = callback
        self.__exchange_name = exchange_name
        self.__exchange_type = exchange_type
        self.__queue_name = queue_name
        self.__routing_key = routing_key
        self.__connection: AbstractRobustConnection | None = None
        self.__channel: AbstractChannel | None = None
        self.__queue: AbstractQueue | None = None
        self.__executor = ThreadPoolExecutor(max_workers=settings.rabbitmq.max_workers)
        self.__message_batch: List[AbstractIncomingMessage] = []
        self.__batch_lock = asyncio.Lock()
        self.__is_running = False

    async def connect(self) -> None:
        """Establish connection to RabbitMQ"""
        try:
            logger.info(
                f"Connecting to RabbitMQ at {settings.rabbitmq.host}:{settings.rabbitmq.port}"
            )
            self.__connection = await connect_robust(settings.rabbitmq.url)
            self.__channel = await self.__connection.channel()

            # Set QoS with prefetch count
            await self.__channel.set_qos(
                prefetch_count=settings.rabbitmq.prefetch_count
            )
            logger.info(f"Set prefetch_count to {settings.rabbitmq.prefetch_count}")

            # Declare exchange
            exchange = await self.__channel.declare_exchange(
                name=self.__exchange_name, type=ExchangeType.TOPIC, durable=True
            )
            logger.info(
                f"Declared exchange: {self.__exchange_name} (type: {self.__exchange_type})"
            )

            # Declare queue
            self.__queue = await self.__channel.declare_queue(
                name=self.__queue_name, durable=True
            )
            logger.info(f"Declared queue: {self.__queue_name}")

            # Bind queue to exchange with routing key
            await self.__queue.bind(exchange=exchange, routing_key=self.__routing_key)
            logger.info(
                f"Bound queue to exchange with routing_key: {self.__routing_key}"
            )

            logger.info("Successfully connected to RabbitMQ")

        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}")
            raise

    async def process_batch(self, batch: List[AbstractIncomingMessage]) -> None:
        """
        Process a batch of messages in a separate thread
        """
        if not batch:
            return

        logger.info(f"Processing batch of {len(batch)} messages")

        # Process batch in thread pool to avoid blocking the event loop
        loop = asyncio.get_event_loop()
        failed_indices = await loop.run_in_executor(
            self.__executor, self._process_batch_sync, batch
        )

        for idx, message in enumerate(batch):
            try:
                if idx in failed_indices:
                    await message.nack(requeue=False)
                    logger.warning(f"Message {idx + 1}/{len(batch)} nacked")
                    continue

                await message.ack()
            except Exception as e:
                logger.error(f"Failed to acknowledge/nack message: {e}")

        logger.info(
            f"Batch of {len(batch)} messages processed: {len(batch) - len(failed_indices)} acked, {len(failed_indices)} nacked"
        )

    def _process_batch_sync(self, batch: List[AbstractIncomingMessage]) -> set[int]:
        """
        Synchronous batch processing (runs in thread pool)

        Returns:
            A set of indices for messages that failed processing
        """
        failed_indices = set()

        for idx, message in enumerate(batch):
            try:
                headers = cast(
                    RabbitmqHeaders,
                    {k: str(v) for k, v in message.headers.items()}
                    if message.headers
                    else {},
                )
                msg = json.loads(message.body.decode("utf-8"))
                self.__callback(msg, headers)
            except json.JSONDecodeError as e:
                logger.error(
                    f"Failed to parse message body as JSON {idx + 1}/{len(batch)}: {e}"
                )
                failed_indices.add(idx)
            except Exception as e:
                logger.error(f"Failed to process message {idx + 1}/{len(batch)}: {e}")
                failed_indices.add(idx)

        return failed_indices

    async def _on_message(self, message: AbstractIncomingMessage) -> None:
        """
        Callback for incoming messages - collects messages into batches
        """
        async with self.__batch_lock:
            self.__message_batch.append(message)
            logger.debug(
                f"Added message to batch (current size: {len(self.__message_batch)})"
            )

            # Process batch when it reaches the configured size
            if len(self.__message_batch) >= settings.rabbitmq.batch_size:
                batch_to_process = self.__message_batch.copy()
                self.__message_batch.clear()

                # Process batch asynchronously (non-blocking)
                asyncio.create_task(self.process_batch(batch_to_process))

    async def start_consuming(self) -> None:
        """Start consuming messages from the queue"""
        if not self.__queue:
            raise RuntimeError("Not connected to RabbitMQ. Call connect() first.")

        self.__is_running = True
        logger.info("Starting message consumption...")

        try:
            # Start consuming messages
            await self.__queue.consume(self._on_message)
            logger.info(f"Consuming messages from queue: {self.__queue_name}")

            # Keep the consumer running
            while self.__is_running:
                await asyncio.sleep(1)

                # Process any remaining messages in batch periodically
                async with self.__batch_lock:
                    if self.__message_batch:
                        logger.info(
                            f"Processing remaining batch of {len(self.__message_batch)} messages"
                        )
                        batch_to_process = self.__message_batch.copy()
                        self.__message_batch.clear()
                        asyncio.create_task(self.process_batch(batch_to_process))

        except asyncio.CancelledError:
            logger.info("Consumer cancelled")
        except Exception as e:
            logger.error(f"Error during message consumption: {e}")
            raise

    async def close(self) -> None:
        """Close RabbitMQ connection and cleanup resources"""
        logger.info("Closing RabbitMQ handler...")
        self.__is_running = False

        # Process any remaining messages in the batch
        async with self.__batch_lock:
            if self.__message_batch:
                logger.info(
                    f"Processing final batch of {len(self.__message_batch)} messages"
                )
                await self.process_batch(self.__message_batch)
                self.__message_batch.clear()

        # Shutdown thread pool
        self.__executor.shutdown(wait=True)
        logger.info("Thread pool executor shut down")

        # Close RabbitMQ connection
        if self.__connection:
            await self.__connection.close()
            logger.info("RabbitMQ connection closed")
