# tests/test_worker_integration.py
#
# Integration tests against real RabbitMQ, Redis, and Postgres containers
# (via testcontainers), proving two things: a worker crash costs at most a
# redelivery, never a lost or duplicated `users` row; and that guarantee
# holds using the exact same `shared_db` models/repository the API queries
# through, not a test-only stand-in.
import threading
import time
import uuid
from collections.abc import Iterator
from contextlib import contextmanager

import pika
import pytest
import redis
from shared_db.db import create_db_engine, create_session_factory
from shared_db.repository import UserRepository

from worker.src.consumer import REDIS_CHANNEL, Worker


class CrashingWorker(Worker):
    """Stands in for a worker process that dies right after doing the
    work but before it can ack, e.g. an OOM kill or a hard `docker kill`."""

    def _process(self, method, _properties, body) -> None:  # type: ignore[override]
        email = body.decode()
        with self._session_factory() as session:
            UserRepository(session).get_or_create(email)
            session.commit()
        self._redis.publish(REDIS_CHANNEL, body)
        raise RuntimeError("simulated crash before ack")


def _publish(amqp_url: str, queue_name: str, body: bytes) -> None:
    connection = pika.BlockingConnection(pika.URLParameters(amqp_url))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)
    channel.basic_publish(
        exchange="",
        routing_key=queue_name,
        body=body,
        properties=pika.BasicProperties(delivery_mode=2),
    )
    connection.close()


@contextmanager
def _redis_subscriber(redis_url: str) -> Iterator[redis.client.PubSub]:
    client = redis.Redis.from_url(redis_url)
    pubsub = client.pubsub()
    pubsub.subscribe(REDIS_CHANNEL)
    pubsub.get_message(timeout=1)  # drain the subscribe confirmation
    try:
        yield pubsub
    finally:
        pubsub.close()


def _wait_for_message(pubsub: redis.client.PubSub, timeout: float = 10.0) -> bytes:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        message = pubsub.get_message(ignore_subscribe_messages=True, timeout=1)
        if message is not None:
            return message["data"]
    raise TimeoutError("no message received on redis channel in time")


def test_worker_persists_user_and_acks_message(
    rabbitmq_url, redis_url, postgres_url, queue_name
):
    """Happy path: one message in, one `users` row upserted via the shared
    repository, one echo on Redis, and the queue drained (acked) rather
    than left pending for redelivery."""
    email = f"{uuid.uuid4().hex[:8]}@example.com".encode()
    _publish(rabbitmq_url, queue_name, email)

    worker = Worker(
        amqp_url=rabbitmq_url,
        redis_url=redis_url,
        queue_name=queue_name,
        database_url=postgres_url,
    )
    thread = threading.Thread(target=worker.run_forever, daemon=True)

    with _redis_subscriber(redis_url) as pubsub:
        thread.start()
        payload = _wait_for_message(pubsub)

    worker.stop()
    thread.join(timeout=5)

    assert payload == email

    engine = create_db_engine(postgres_url)
    with create_session_factory(engine)() as session:
        user = UserRepository(session).get_by_email(email.decode())
        assert user is not None
        assert user.email == email.decode()


def test_worker_crash_before_ack_does_not_duplicate_user(
    rabbitmq_url, redis_url, postgres_url, queue_name
):
    """This is the scenario a thread-in-API-process consumer makes painful
    to reason about. Because the worker is its own process talking to a
    durable queue with manual ack, a crash only costs a redelivery, never
    the message; and because the shared repository's `get_or_create` is
    idempotent, that redelivery does not create a duplicate `users` row
    even though the email gets processed twice. Recovering from the crash
    does not touch the API process at all.
    """
    email = f"{uuid.uuid4().hex[:8]}@example.com".encode()
    _publish(rabbitmq_url, queue_name, email)

    crashing_worker = CrashingWorker(
        amqp_url=rabbitmq_url,
        redis_url=redis_url,
        queue_name=queue_name,
        database_url=postgres_url,
    )
    with pytest.raises(RuntimeError):
        crashing_worker.run_forever()

    # The broker only requeues an unacked message once the channel/connection
    # is gone, exactly as would happen if this process had been OOM-killed.
    assert crashing_worker._connection is not None
    crashing_worker._connection.close()

    # A fresh worker instance, standing in for a restarted replica, must
    # still pick up the redelivered message with nothing lost.
    recovered_worker = Worker(
        amqp_url=rabbitmq_url,
        redis_url=redis_url,
        queue_name=queue_name,
        database_url=postgres_url,
    )
    thread = threading.Thread(target=recovered_worker.run_forever, daemon=True)

    with _redis_subscriber(redis_url) as pubsub:
        thread.start()
        payload = _wait_for_message(pubsub)

    recovered_worker.stop()
    thread.join(timeout=5)

    assert payload == email

    engine = create_db_engine(postgres_url)
    with create_session_factory(engine)() as session:
        repository = UserRepository(session)
        assert repository.count_by_email(email.decode()) == 1
