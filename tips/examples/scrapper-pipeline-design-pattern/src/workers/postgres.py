"""Worker pool that persists price messages into Postgres."""

from __future__ import annotations

import os
import threading
from queue import Empty, Queue
from typing import Literal

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

Symbol = str
Price = float
PriceMessage = tuple[Symbol, Price, str]
Sentinel = Literal["DONE"]


class PostgresMasterScheduler(threading.Thread):
    """Consumes price messages from a queue and writes each one to Postgres."""

    def __init__(
        self, input_queue: "Queue[PriceMessage | Sentinel]", **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self._input_queue = input_queue
        self.start()

    def run(self) -> None:
        while True:
            try:
                val = self._input_queue.get(timeout=20)
            except Empty:
                print("Timeout reached in Postgres scheduler, stopping...")
                break

            if val == "DONE":
                break

            symbol, price, extracted_time = val
            worker = PostgresWorker(symbol, price, extracted_time)
            worker.insert_into_db()


class PostgresWorker:
    """Inserts a single price observation into the `prices` table."""

    _create_table_lock = threading.Lock()
    """
    Needed for when we have multiple threads trying to create the table.
    Note: the IF NOT EXISTS check isn't atomic for the implicit SERIAL sequence,
    so when several threads hit it concurrently on first run,
    they all try to create prices_id_seq and one loses with UniqueViolation. 
    """

    def __init__(self, symbol: Symbol, price: Price, extracted_time: str) -> None:
        self._symbol = symbol
        self._price = price
        self._extracted_time = extracted_time

        self._pg_user: str = os.environ.get("POSTGRES_USER", "")
        self._pg_pw: str = os.environ.get("POSTGRES_PASSWORD", "")
        self._pg_host: str = os.environ.get("PG_HOST", "localhost")
        self._pg_port: str = os.environ.get("POSTGRESQL_EXPOSED_PORT", "5432")
        self._pg_db: str = os.environ.get("POSTGRES_DB", "postgres")

        self._engine = create_engine(
            f"postgresql://{self._pg_user}:{self._pg_pw}@{self._pg_host}:{self._pg_port}/{self._pg_db}"
        )

    def _create_table_if_missing(self) -> None:
        create_table_query = """
            CREATE TABLE IF NOT EXISTS prices (
                id           SERIAL PRIMARY KEY,
                symbol       TEXT,
                price        DOUBLE PRECISION,
                insert_time  TIMESTAMPTZ
            )
        """
        with self._create_table_lock, self._engine.connect() as conn:
            conn.execute(text(create_table_query))
            conn.commit()

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