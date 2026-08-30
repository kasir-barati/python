"""Worker pool that fetches live prices from Yahoo Finance."""

from __future__ import annotations

import random
import threading
import time
from datetime import UTC, datetime
from queue import Empty, Queue
from typing import Literal

import requests
from lxml import html

Symbol = str
Price = float
PriceMessage = tuple[Symbol, Price, str]
Sentinel = Literal["DONE"]


class YahooFinancePriceScheduler(threading.Thread):
    """
    Pulls ticker symbols off an input queue and fans price results out
    to one or more output queues.
    """

    def __init__(
        self,
        input_queue: "Queue[Symbol | Sentinel]",
        output_queues: list["Queue[PriceMessage | Sentinel]"],
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self._input_queue = input_queue
        self._output_queues = output_queues
        self.start()

    def run(self) -> None:
        while True:
            # Defensive programming: protects this scheduler from hanging
            # indefinitely. Trade-off: if a message arrives right after the
            # timeout fires, it's dropped without ever being processed.
            try:
                val = self._input_queue.get(timeout=20)
            except Empty:
                print("Timeout reached in Yahoo Finance scheduler, stopping...")
                break

            if val == "DONE":
                for output_queue in self._output_queues:
                    output_queue.put("DONE")
                break

            worker = YahooFinancePriceWorker(symbol=val)
            price = worker.get_price()
            if price is None:
                continue

            message: PriceMessage = (val, price, str(datetime.now(UTC)))
            for output_queue in self._output_queues:
                output_queue.put(message)

            time.sleep(random.random())  # Cloudflare may block bursty requests


class YahooFinancePriceWorker:
    """Fetches the current price for a single ticker symbol."""

    def __init__(self, symbol: Symbol, **kwargs) -> None:
        self._symbol = symbol
        base_url = "https://finance.yahoo.com/quote/"
        self._url = f"{base_url}{self._symbol}"
        self._headers: dict[str, str] = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
            )
        }

    def get_price(self) -> Price | None:
        """Return the current price, or None if the request/parse fails."""
        response = requests.get(self._url, headers=self._headers)
        if response.status_code != 200:
            return None

        page_contents = html.fromstring(response.text)
        nodes = page_contents.xpath('//*[@data-testid="qsp-price"]')
        if not nodes:
            return None

        raw_price = nodes[0].text
        return float(raw_price.strip().replace(",", ""))
