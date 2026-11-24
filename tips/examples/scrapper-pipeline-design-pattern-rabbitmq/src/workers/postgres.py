"""Worker that persists price messages pulled off RabbitMQ into Postgres."""

from __future__ import annotations

import json
import signal

import pika
from sqlalchemy import create_engine, text

from config import config
from pipelines.reader import PipelineTopology

Symbol = str
Price = float
PriceMessage = tuple[Symbol, Price, str]

# Arbitrary shared key for the `prices` table creation advisory lock (see PostgresWorker).
PRICES_TABLE_LOCK_KEY = 727_500


class PostgresMasterScheduler:
    """Consumes price messages from RabbitMQ and writes each one to Postgres."""

    def __init__(self, topology: PipelineTopology, worker_name: str) -> None:
        self._input_queue = topology.input_queue_name(worker_name)
        self._topology = topology

    def run(self) -> None:
        connection = pika.BlockingConnection(pika.URLParameters(config.rabbitmq_url))
        channel = connection.channel()
        self._topology.declare(channel)
        channel.basic_qos(prefetch_count=1)

        # Whether the queue is ever "done" is a fleet-wide fact this process can't see (another
        # replica may still be running, or a scale-up may add more later) - so run until told to
        # stop. In production that's a SIGTERM from Kubernetes/KEDA scaling this replica down.
        signal.signal(signal.SIGTERM, lambda *_args: channel.stop_consuming())

        def on_message(channel, method_frame, _properties, body) -> None:
            symbol, price, extracted_time = json.loads(body)
            PostgresWorker(symbol, price, extracted_time).insert_into_db()
            channel.basic_ack(delivery_tag=method_frame.delivery_tag)

        channel.basic_consume(queue=self._input_queue, on_message_callback=on_message)
        channel.start_consuming()
        connection.close()


class PostgresWorker:
    """Inserts a single price observation into the `prices` table."""

    def __init__(self, symbol: Symbol, price: Price, extracted_time: str) -> None:
        self._symbol = symbol
        self._price = price
        self._extracted_time = extracted_time
        self._engine = create_engine(config.postgres_url)

    def _create_table_if_missing(self) -> None:
        """
        Several PostgresWorker containers can race to create the table on first run,
        the IF NOT EXISTS check isn't atomic for the implicit SERIAL sequence. A Postgres
        advisory lock serializes them across processes (the in-process threading.Lock this
        replaces only worked because the original pipeline ran every instance in one process).
        """
        create_table_query = """
            CREATE TABLE IF NOT EXISTS prices (
                id           SERIAL PRIMARY KEY,
                symbol       TEXT,
                price        DOUBLE PRECISION,
                insert_time  TIMESTAMPTZ
            )
        """
        with self._engine.connect() as conn:
            conn.execute(text("SELECT pg_advisory_lock(:key)"), {"key": PRICES_TABLE_LOCK_KEY})
            try:
                conn.execute(text(create_table_query))
                conn.commit()
            finally:
                conn.execute(text("SELECT pg_advisory_unlock(:key)"), {"key": PRICES_TABLE_LOCK_KEY})

    def insert_into_db(self) -> None:
        self._create_table_if_missing()

        insert_query = """
            INSERT INTO prices (symbol, price, insert_time)
            VALUES (:symbol, :price, CAST(:extracted_time AS TIMESTAMP))
        """
        with self._engine.connect() as conn:
            conn.execute(
                text(insert_query),
                {
                    "symbol": self._symbol,
                    "price": self._price,
                    "extracted_time": self._extracted_time,
                },
            )
            conn.commit()
