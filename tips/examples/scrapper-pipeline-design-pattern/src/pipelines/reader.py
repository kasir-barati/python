import importlib
import threading

import yaml
from multiprocessing import Queue


class YamlPipelineExecutor(threading.Thread):
    def __init__(self, pipeline_location: str, **kwargs):
        super().__init__(**kwargs)
        self._pipeline_location = pipeline_location
        self._queues: dict[str, Queue] = {}
        self._workers: dict[str, list[threading.Thread]] = {}
        self._queue_consumers: dict[str, int] = {}
        self._downstream_queues: dict[str, list[str]] = {}

    def _load_pipeline(self):
        with open(self._pipeline_location,'r') as in_file:
            self._yaml_data=yaml.safe_load(in_file)

    def _initialize_queues(self):
        for queue in self._yaml_data['queues']:
            queue_name: str = queue['name']
            self._queues[queue_name] = Queue()

    def _initialize_workers(self):
        for worker in self._yaml_data['workers']:
            WorkerClass = getattr(importlib.import_module(worker['location']),worker['class'])
            input_queue: str = worker.get('input_queue')
            output_queues: list[str] = worker.get('output_queues')
            input_values: list[str] = worker.get('input_values')
            worker_name: str = worker.get('name')
            number_of_instances: int = worker.get('instances', 1)

            self._downstream_queues[worker_name] = output_queues
            if input_queue is not None:
                self._queue_consumers[input_queue] = number_of_instances

            # Making sure we are NOT adding kwargs which was NOT specified in the yaml file
            init_params: dict[str] = {}
            if input_queue is not None:
                init_params['input_queue'] = self._queues[input_queue]
            if output_queues is not None:
                init_params['output_queues'] = [self._queues[queue_name] for queue_name in output_queues]
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
                if total_worker_threads_alive == 0:
                    if self._downstream_queues[worker_name] is not None:
                        for output_queue in self._downstream_queues[worker_name]:
                            number_of_consumers = self._queue_consumers[output_queue]
                            for i in range(number_of_consumers):
                                self._queues[output_queue].put("DONE")

                    delete_these_workers.append(worker_name)

            print(f"{worker_name} has {total_worker_threads_alive} active threads")

            for queue_name in self._queues:
                print(f"{queue_name} has {self._queues[queue_name].qsize()} messages in it")

            for worker_name in delete_these_workers:
                del self._workers[worker_name]

            if total_workers_alive == 0:
                break