"""Scrapes the current S&P 500 constituent list from Wikipedia and publishes each ticker to RabbitMQ."""

from __future__ import annotations

from collections.abc import Iterator

import pika
import requests
from bs4 import BeautifulSoup

from config import config
from pipelines.reader import PipelineTopology


class WikiWorkerMasterScheduler:
    """Runs the WikiWorker once against every configured URL and publishes the results."""

    def __init__(self, topology: PipelineTopology, worker_name: str) -> None:
        self._topology = topology
        self._input_values: list[str] = topology.worker(worker_name)["input_values"]
        self._output_targets = topology.output_targets(worker_name)

    def run(self) -> None:
        connection = pika.BlockingConnection(pika.URLParameters(config.rabbitmq_url))
        channel = connection.channel()
        self._topology.declare(channel)

        for input_value in self._input_values:
            for symbol in WikiWorker(input_value).get_sp_500_companies():
                for exchange, routing_key in self._output_targets:
                    channel.basic_publish(
                        exchange=exchange,
                        routing_key=routing_key,
                        body=symbol.encode(),
                        properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent),
                    )

        connection.close()


class WikiWorker:
    """Fetches and parses the S&P 500 constituents table from Wikipedia."""

    def __init__(self, url: str) -> None:
        self._url: str = url
        self._headers: dict[str, str] = {
            "User-Agent": "wiki-yahoo-scraper/0.1 (educational/demo project; contact: set-your-contact-info-here)"
        }

    @staticmethod
    def _extract_company_symbols(page_html: str) -> Iterator[str]:
        """Yield ticker symbols parsed out of the constituents table HTML."""
        soup = BeautifulSoup(page_html, "html.parser")
        table = soup.find(id="constituents")
        table_rows = table.find_all("tr")

        for table_row in table_rows[1:]:
            symbol: str = table_row.find("td").text.strip("\n")
            yield symbol

    def get_sp_500_companies(self) -> Iterator[str]:
        """Yield each S&P 500 ticker symbol, or nothing on request failure."""
        response = requests.get(self._url, headers=self._headers)
        if response.status_code != 200:
            print("Couldn't get entries")
            return

        yield from self._extract_company_symbols(response.text)
