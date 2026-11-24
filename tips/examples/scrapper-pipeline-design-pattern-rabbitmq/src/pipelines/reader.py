"""Reads the pipeline YAML and resolves the RabbitMQ topology (queue/exchange names) each worker stage needs."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Literal, NotRequired, TypedDict

import yaml

if TYPE_CHECKING:
    from pika.adapters.blocking_connection import BlockingChannel

QueueMode = Literal["direct", "fanout"]


class QueueSpec(TypedDict):
    name: str
    description: NotRequired[str]
    mode: NotRequired[QueueMode]


WorkerSpec = TypedDict(
    "WorkerSpec",
    {
        "name": str,
        "description": NotRequired[str],
        "location": str,
        "class": str,
        "instances": NotRequired[int],
        "input_queue": NotRequired[str],
        "output_queues": NotRequired[list[str]],
        "input_values": NotRequired[list[str]],
    },
)


class PipelineSpec(TypedDict):
    queues: list[QueueSpec]
    workers: list[WorkerSpec]


class PipelineTopology:
    """
    Maps the logical queues declared in the pipeline YAML onto physical RabbitMQ
    queues/exchanges. `direct` queues are one quorum queue shared by every instance
    of the single subscribing stage (competing consumers). `fanout` queues become a
    fanout exchange with one quorum queue per subscribing stage, so every stage sees
    every message while instances within a stage still compete for their own copy.
    """

    def __init__(self, pipeline_location: Path) -> None:
        with open(pipeline_location) as in_file:
            self._spec: PipelineSpec = yaml.safe_load(in_file)

        self._queue_modes: dict[str, QueueMode] = {
            queue["name"]: queue.get("mode", "direct") for queue in self._spec["queues"]
        }
        self._workers_by_name = {worker["name"]: worker for worker in self._spec["workers"]}

        subscribers: dict[str, list[str]] = {}
        for worker in self._spec["workers"]:
            input_queue = worker.get("input_queue")
            if input_queue is not None:
                subscribers.setdefault(input_queue, []).append(worker["name"])

        for queue_name, subscriber_names in subscribers.items():
            if self._queue_modes.get(queue_name, "direct") == "direct" and len(subscriber_names) > 1:
                raise ValueError(
                    f"Queue '{queue_name}' is consumed by multiple worker stages "
                    f"({', '.join(subscriber_names)}) but is NOT marked 'mode: fanout' "
                    f"in the pipeline YAML."
                )

        self._subscribers = subscribers

    def worker(self, worker_name: str) -> WorkerSpec:
        return self._workers_by_name[worker_name]

    def input_queue_name(self, worker_name: str) -> str:
        """Physical RabbitMQ queue this worker stage should consume from."""
        logical_queue = self._workers_by_name[worker_name]["input_queue"]
        if self._queue_modes.get(logical_queue, "direct") == "fanout":
            return f"{logical_queue}.{worker_name}"
        return logical_queue

    def output_targets(self, worker_name: str) -> list[tuple[str, str]]:
        """(exchange, routing_key) pairs this worker stage should publish its results to."""
        targets = []
        for logical_queue in self._workers_by_name[worker_name].get("output_queues") or []:
            if self._queue_modes.get(logical_queue, "direct") == "fanout":
                targets.append((logical_queue, ""))
            else:
                targets.append(("", logical_queue))
        return targets

    def declare(self, channel: "BlockingChannel") -> None:
        """Idempotently declares every quorum queue (and fanout exchange) in the pipeline."""
        for logical_queue, mode in self._queue_modes.items():
            if mode == "fanout":
                channel.exchange_declare(exchange=logical_queue, exchange_type="fanout", durable=True)
                for subscriber_name in self._subscribers.get(logical_queue, []):
                    queue_name = f"{logical_queue}.{subscriber_name}"
                    channel.queue_declare(queue=queue_name, durable=True, arguments={"x-queue-type": "quorum"})
                    channel.queue_bind(exchange=logical_queue, queue=queue_name)
            else:
                channel.queue_declare(queue=logical_queue, durable=True, arguments={"x-queue-type": "quorum"})
