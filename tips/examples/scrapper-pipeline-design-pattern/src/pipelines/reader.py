import importlib
import threading
import time
from typing import NotRequired, TypedDict, Literal

import yaml
from multiprocessing import Queue


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


class InitParam(TypedDict):
    input_values: NotRequired[list[str]]
    input_queue: NotRequired[Queue]
    output_queues: NotRequired[list[Queue]]

class YamlPipelineExecutor(threading.Thread):
    def __init__(self, pipeline_location: str, **kwargs):
        super().__init__(**kwargs)
        self._pipeline_location = pipeline_location
        # queue_name -> {worker_name: physical Queue dedicated to that subscriber}
        self._queue_subscriber_queues: dict[str, dict[str, Queue]] = {}
        self._queue_modes: dict[str, QueueMode] = {}
        self._workers: dict[str, list[threading.Thread]] = {}
        # queue_name -> [(physical Queue, number_of_consumer_instances), ...one entry per subscribing stage]
        self._queue_consumers: dict[str, list[tuple[Queue, int]]] = {}
        self._downstream_queues: dict[str, list[str]] = {}

    def _load_pipeline(self):
        with open(self._pipeline_location,'r') as in_file:
            self._yaml_data: PipelineSpec = yaml.safe_load(in_file)

    def _initialize_queues(self):
        for queue in self._yaml_data['queues']:
            queue_name = queue['name']
            self._queue_modes[queue_name] = queue.get('mode', 'direct')

        subscribers: dict[str, list[str]] = {}
        for worker in self._yaml_data['workers']:
            input_queue = worker.get('input_queue')
            if input_queue is not None:
                subscribers.setdefault(input_queue, []).append(worker['name'])

        for queue_name, subscriber_names in subscribers.items():
            mode = self._queue_modes.get(queue_name, 'direct')
            if mode == 'direct' and len(subscriber_names) > 1:
                raise ValueError(
                    f"Queue '{queue_name}' is consumed by multiple worker stages "
                    f"({', '.join(subscriber_names)}) but is NOT marked 'mode: fanout' "
                    f"in the pipeline YAML. Either give each stage its own queue, or "
                    f"set mode: fanout on '{queue_name}' to broadcast to all of them."
                )

            self._queue_subscriber_queues[queue_name] = {
                worker_name: Queue() for worker_name in subscriber_names
            }

    def _initialize_workers(self):
        for worker in self._yaml_data['workers']:
            WorkerClass = getattr(importlib.import_module(worker['location']),worker['class'])
            input_queue: str = worker.get('input_queue')
            output_queues: list[str] = worker.get('output_queues')
            input_values: list[str] = worker.get('input_values')
            worker_name: str = worker.get('name')
            number_of_instances: int = worker.get('instances', 1)

            self._downstream_queues[worker_name] = output_queues

            init_params: InitParam = {}
            if input_queue is not None:
                own_queue = self._queue_subscriber_queues[input_queue][worker_name]
                init_params['input_queue'] = own_queue
                self._queue_consumers.setdefault(input_queue, []).append((own_queue, number_of_instances))
            if output_queues is not None:
                init_params['output_queues'] = [
                    subscriber_queue
                    for queue_name in output_queues
                    for subscriber_queue in self._queue_subscriber_queues[queue_name].values()
                ]
            if input_values is not None:
                init_params['input_values'] = input_values

            self._workers[worker_name] = []
            for i in range(number_of_instances):
                self._workers[worker_name].append(WorkerClass(**init_params))


    def _process_pipeline(self):
        self._load_pipeline()
        self._initialize_queues()
        self._initialize_workers()

    def run(self):
        self._process_pipeline()

        while True:
            total_workers_alive = 0
            delete_these_workers = []

            for worker_name in self._workers:
                total_worker_threads_alive = 0
                for worker_thread in self._workers[worker_name]:
                    if worker_thread.is_alive():
                        total_worker_threads_alive += 1

                total_workers_alive += total_worker_threads_alive
                print(f"{worker_name} has {total_worker_threads_alive} active threads")

                if total_worker_threads_alive == 0:
                    if self._downstream_queues[worker_name] is not None:
                        for output_queue in self._downstream_queues[worker_name]:
                            subscribers = self._queue_consumers.get(output_queue, [])

                            if not subscribers:
                                print(f"Investigate why {output_queue} has no consumer, is this a bug or intentional behavior?")

                            for physical_queue, number_of_consumers in subscribers:
                                for i in range(number_of_consumers):
                                    physical_queue.put("DONE")

                    delete_these_workers.append(worker_name)

            for queue_name, subscriber_queues in self._queue_subscriber_queues.items():
                for worker_name, physical_queue in subscriber_queues.items():
                    print(f"{queue_name} -> {worker_name} has {physical_queue.qsize()} messages in it")

            for worker_name in delete_these_workers:
                del self._workers[worker_name]

            if total_workers_alive == 0:
                break

            time.sleep(0.1)
