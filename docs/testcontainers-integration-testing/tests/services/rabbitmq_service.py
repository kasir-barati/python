import asyncio
import json
from typing import Dict, Any, Optional, List
from aio_pika import connect_robust, Channel, Exchange, Queue, Message
from aio_pika.abc import AbstractRobustConnection


class RabbitmqService:
    """Service class for RabbitMQ operations."""

    __slots__ = ["connection_url", "__connection", "__channel"]

    def __init__(self, connection_url: str):
        self.connection_url = connection_url
        self.__connection: Optional[AbstractRobustConnection] = None
        self.__channel: Optional[Channel] = None

    async def connect(self) -> None:
        """Establish connection to RabbitMQ."""
        self.__connection = await connect_robust(self.connection_url)
        self.__channel = await self.__connection.channel()

    async def disconnect(self) -> None:
        """Close connection to RabbitMQ."""
        if self.__connection and not self.__connection.is_closed:
            await self.__connection.close()

    async def declare_exchange(
        self, name: str, exchange_type: str = "direct"
    ) -> Exchange:
        """Declare an exchange."""
        if not self.__channel:
            raise RuntimeError("Not connected to RabbitMQ")

        from aio_pika import ExchangeType

        # Map string to ExchangeType enum
        type_mapping = {
            "direct": ExchangeType.DIRECT,
            "fanout": ExchangeType.FANOUT,
            "topic": ExchangeType.TOPIC,
            "headers": ExchangeType.HEADERS,
        }
        exchange_type_enum = type_mapping.get(
            exchange_type.lower(), ExchangeType.DIRECT
        )

        return await self.__channel.declare_exchange(
            name, type=exchange_type_enum, durable=True
        )

    async def declare_queue(self, name: str) -> Queue:
        """Declare a queue."""
        if not self.__channel:
            raise RuntimeError("Not connected to RabbitMQ")

        return await self.__channel.declare_queue(name, durable=True)

    async def bind_queue(
        self, queue: Queue, exchange: Exchange, routing_key: str
    ) -> None:
        """Bind queue to exchange with routing key."""
        await queue.bind(exchange, routing_key)

    async def publish_message(
        self, exchange_name: str, routing_key: str, message: Dict[str, Any]
    ) -> None:
        """Publish a message to an exchange."""
        if not self.__channel:
            raise RuntimeError("Not connected to RabbitMQ")

        exchange = await self.declare_exchange(exchange_name)
        message_body = json.dumps(message).encode()

        await exchange.publish(Message(message_body), routing_key=routing_key)

    async def consume_messages(
        self, queue_name: str, max_messages: int = 1, timeout: float = 5.0
    ) -> List[Dict[str, Any]]:
        """Consume messages from a queue."""
        if not self.__channel:
            raise RuntimeError("Not connected to RabbitMQ")

        queue = await self.declare_queue(queue_name)
        messages = []

        try:
            async with asyncio.timeout(timeout):
                async with queue.iterator() as queue_iter:
                    async for message in queue_iter:
                        async with message.process():
                            message_data = json.loads(message.body.decode())
                            messages.append(message_data)

                            if len(messages) >= max_messages:
                                break
        except asyncio.TimeoutError:
            pass  # Return whatever messages we got

        return messages

    async def get_queue_message_count(self, queue_name: str) -> int:
        """Get the number of messages in a queue."""
        if not self.__channel:
            raise RuntimeError("Not connected to RabbitMQ")

        # Use passive declare to get queue info without affecting the queue
        queue_info = await self.__channel.declare_queue(queue_name, passive=True)

        return queue_info.message_count
