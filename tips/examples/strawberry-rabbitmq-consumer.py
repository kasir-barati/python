"""
RabbitMQ queue -> consumer thread (daemon) -> Redis pub/sub -> Strawberry subscription -> GraphQL client
"""

import signal
import threading
from collections.abc import AsyncGenerator
from types import FrameType

import pika
import redis
import redis.asyncio as aioredis
import strawberry
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties
from strawberry.asgi import GraphQL

# src/messaging/broadcaster.py
#
# Bridge between the (sync) pika consumer thread and the (async) GraphQL subscription resolvers, via Redis pub/sub instead of an in-process queue.
# This is what lets multiple API replicas each pick up the RabbitMQ message once and still have every subscriber, on every replica, see it.
REDIS_URL = "redis://localhost:6379/0"
REDIS_CHANNEL = "queue_messages"
redis_client: redis.Redis = redis.Redis.from_url(REDIS_URL)


# src/messaging/consumer.py
#
# Owns the RabbitMQ connection/channel and the shutdown signal. Kept as a class (rather than a bare function + globals) so main.py can call `.stop()` from a signal handler without reaching into module internals.
class RabbitmqConsumer:
    def __init__(self, amqp_url: str, queue_name: str) -> None:
        self._amqp_url = amqp_url
        self._queue_name = queue_name
        self._connection: pika.BlockingConnection | None = None
        self._channel: BlockingChannel | None = None

    def run(self) -> None:
        self._connection = pika.BlockingConnection(pika.URLParameters(self._amqp_url))
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=self._queue_name, durable=True)
        self._channel.basic_consume(
            queue=self._queue_name,
            on_message_callback=self._on_message,
        )
        try:
            self._channel.start_consuming()
        except Exception:
            # Not attempting a reconnect here to keep the example short.
            # A production consumer would retry with backoff and log/alert
            # instead of letting the thread die silently.
            raise

    def stop(self) -> None:
        # start_consuming()/basic_consume() are blocking-connection APIs,
        # so we must schedule the stop on the connection's own thread.
        if self._connection is not None and self._channel is not None:
            self._connection.add_callback_threadsafe(self._channel.stop_consuming)

    def _on_message(
        self,
        channel: BlockingChannel,
        method: Basic.Deliver,
        _properties: BasicProperties,
        body: bytes,
    ) -> None:
        redis_client.publish(REDIS_CHANNEL, body)
        channel.basic_ack(delivery_tag=method.delivery_tag)


# src/graphql/subscriptions.py
@strawberry.type
class Subscription:
    @strawberry.subscription
    async def queue_messages(self) -> AsyncGenerator[str, None]:
        aio_redis_client = aioredis.Redis.from_url(REDIS_URL)
        async with aio_redis_client.pubsub() as pubsub:
            await pubsub.subscribe(REDIS_CHANNEL)
            while True:
                message = await pubsub.get_message(
                    ignore_subscribe_messages=True, timeout=None
                )
                if message is not None:
                    yield message["data"].decode()


# src/graphql/queries.py
@strawberry.type
class Query:
    @strawberry.field
    def health(self) -> str:
        return "ok"


# src/graphql/schema.py
schema = strawberry.Schema(query=Query, subscription=Subscription)


# src/main.py
consumer = RabbitmqConsumer(amqp_url="amqp://guest:guest@localhost/", queue_name="tasks")
consumer_thread = threading.Thread(target=consumer.run, daemon=True)


def _handle_shutdown(_signum: int, _frame: FrameType | None) -> None:
    # Ask pika to stop consuming, then give the thread a bounded window to drain the in-flight message before we let it be daemon-killed.
    # This is the "graceful shutdown" half `daemon=True` doesn't give you for free.
    #
    # Plain strawberry.asgi.GraphQL has no lifespan/startup-shutdown hooks of its own (Starlette/FastAPI has one tho), so SIGTERM/SIGINT are the hook point here instead.
    consumer.stop()
    consumer_thread.join(timeout=5)


signal.signal(signal.SIGTERM, _handle_shutdown)
signal.signal(signal.SIGINT, _handle_shutdown)

consumer_thread.start()

app = GraphQL(schema)
