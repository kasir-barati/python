"""Worker that fetches live prices from Yahoo Finance for tickers pulled off RabbitMQ."""

from __future__ import annotations

import json
import random
import signal
import time
from datetime import UTC, datetime

import pika
import requests
from lxml import html

from config import config
from pipelines.reader import PipelineTopology

Symbol = str
Price = float
PriceMessage = tuple[Symbol, Price, str]


class YahooFinancePriceScheduler:
    """Pulls ticker symbols off its input queue and fans price results out to its output queues."""

    def __init__(self, topology: PipelineTopology, worker_name: str) -> None:
        self._input_queue = topology.input_queue_name(worker_name)
        self._output_targets = topology.output_targets(worker_name)
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
            symbol = body.decode()
            price = YahooFinancePriceWorker(symbol=symbol).get_price()
            if price is not None:
                message: PriceMessage = (symbol, price, str(datetime.now(UTC)))
                for exchange, routing_key in self._output_targets:
                    channel.basic_publish(
                        exchange=exchange,
                        routing_key=routing_key,
                        body=json.dumps(message).encode(),
                        properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent),
                    )

            channel.basic_ack(delivery_tag=method_frame.delivery_tag)
            time.sleep(random.random())  # Cloudflare may block bursty requests

        channel.basic_consume(queue=self._input_queue, on_message_callback=on_message)
        channel.start_consuming()
        connection.close()


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
