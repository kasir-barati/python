"""Scrapes the current S&P 500 constituent list from Wikipedia."""

from collections.abc import Iterator
from queue import Empty, Queue
from typing import Literal
import threading

import requests
from bs4 import BeautifulSoup


Sentinel = Literal["DONE"]


class WikiWorkerMasterScheduler(threading.Thread):
    def __init__(self, input_values: list[str], output_queues: list["Queue[str | Sentinel]"], **kwargs):
        self._input_values = input_values
        self._output_queues = output_queues
        super().__init__(**kwargs)
        self.start()

    def run(self):
        for input_value in self._input_values:
            wiki_worker = WikiWorker(input_value)
            for symbol in wiki_worker.get_sp_500_companies():
                for output_queue in self._output_queues:
                    output_queue.put(symbol)
                # break  # 👈 if you want a quick and dirty test UNCOMMENT ME

        for output_queue in self._output_queues:
            output_queue.put("DONE")

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
