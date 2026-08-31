"""Wires the wiki -> Yahoo Finance -> Postgres pipeline together and runs it."""

from __future__ import annotations

import time
from pathlib import Path

from pipelines.reader import YamlPipelineExecutor


def main() -> None:
    scraper_start_time = time.time()
    pipeline_location = Path(__file__).parent / 'pipelines' / 'wiki_yahoo_scraper_pipeline.yaml'
    yaml_pipeline_executor = YamlPipelineExecutor(pipeline_location=pipeline_location)
    yaml_pipeline_executor.start()
    
    elapsed = time.time() - scraper_start_time

    print(f"Finished in {elapsed:.2f}s")


if __name__ == "__main__":
    main()