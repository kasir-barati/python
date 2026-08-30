import logging
import os
import signal
from types import FrameType

import pika
import redis
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties
from shared_db.db import create_db_engine, create_session_factory, init_db
from shared_db.repository import UserRepository

logging.basicConfig(level=logging.INFO, format="%(asctime)s worker: %(message)s")
logger = logging.getLogger("worker")

REDIS_CHANNEL = "queue_messages"


class Worker:
    """
    Consumes `queue_name` from RabbitMQ.
    Each message body is treated as a user's email address:
    - It upserts them into the `users` table.
    - The raw body is republished onto a Redis pub/sub channel for the subscription API.

    Durable queue + manual ack (no `auto_ack`) is what makes this safe to crash:
    - Unacked messages are simply redelivered to whichever consumer reconnects next.
    - `get_or_create` makes the redelivery safe, reprocessing the same email is a no-op, not a duplicate row.
    """

    def __init__(
        self, amqp_url: str, redis_url: str, queue_name: str, database_url: str
    ) -> None:
        self._amqp_url = amqp_url
        self._queue_name = queue_name
        self._redis: redis.Redis = redis.Redis.from_url(redis_url)
        self._connection: pika.BlockingConnection | None = None
        self._channel: BlockingChannel | None = None
        self._should_run = True

        engine = create_db_engine(database_url)
        init_db(engine)
        self._session_factory = create_session_factory(engine)

    def connect(self) -> None:
        self._connection = pika.BlockingConnection(pika.URLParameters(self._amqp_url))
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=self._queue_name, durable=True)
        # One in-flight message per consumer at a time + manual ack:
        # - How much work is lost/redelivered on a crash.
        # - The throughput knob you'd tune independently.
        self._channel.basic_qos(prefetch_count=1)

    def run_forever(self) -> None:
        self.connect()
        assert self._channel is not None
        # Keep asking RabbitMQ for the next message.
        # Every second, even if there is no message, give me control back so I can check whether I should shut down.
        for method, properties, body in self._channel.consume(
            self._queue_name, inactivity_timeout=1
        ):
            if not self._should_run:
                break
            if method is None:
                continue
            self._process(method, properties, body)

    def stop(self) -> None:
        self._should_run = False

    def _process(
        self, method: Basic.Deliver, _properties: BasicProperties, body: bytes
    ) -> None:
        email = body.decode()

        with self._session_factory() as session:
            repository = UserRepository(session)
            user = repository.get_or_create(email)
            session.commit()
            logger.info("Upserted user id=%s email=%s", user.id, user.email)

        self._redis.publish(REDIS_CHANNEL, body)
        assert self._channel is not None
        self._channel.basic_ack(delivery_tag=method.delivery_tag)


def _install_signal_handlers(worker: Worker) -> None:
    def handle(_signum: int, _frame: FrameType | None) -> None:
        logger.info("shutdown signal received, draining current message")
        worker.stop()

    signal.signal(signal.SIGTERM, handle)
    signal.signal(signal.SIGINT, handle)


def main() -> None:
    worker = Worker(
        amqp_url=os.environ.get("AMQP_URL", "amqp://guest:guest@localhost:5672/"),
        redis_url=os.environ.get("REDIS_URL", "redis://localhost:6379/0"),
        queue_name=os.environ.get("QUEUE_NAME", "tasks"),
        database_url=os.environ.get(
            "DATABASE_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/app"
        ),
    )
    _install_signal_handlers(worker)
    worker.run_forever()


if __name__ == "__main__":
    main()
