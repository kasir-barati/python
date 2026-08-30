import importlib

import yaml
from multiprocessing import Queue


class YamlPipelineExecutor():
    def __init__(self, pipeline_location: str):
        self._pipeline_location = pipeline_location
        self._queues={}
        self._workers={}

    def _load_pipeline(self):
        with open(self._pipeline_location,'r') as in_file:
            self._yaml_data=yaml.safe_load(in_file)

    def _initialize_queues(self):
        for queue in self._yaml_data['queues']:
            queue_name=queue['name']
            self._queues[queue_name]=Queue()

    def _initialize_workers(self):
        for worker in self._yaml_data['workers']:
            WorkerClass = getattr(importlib.import_module(worker['location']),worker['class'])
            input_queue = worker.get('input_queue')
            output_queues = worker.get('output_queues')
            input_values = worker.get('input_values')
            worker_name = worker.get('name')
            number_of_instances = worker.get('instances', 1)

            # Making sure we are NOT adding kwargs which was NOT specified in the yaml file
            init_params = {}
            if input_queue is not None:
                init_params['input_queue'] = self._queues[input_queue]
            if output_queues is not None:
                init_params['output_queues'] = [self._queues[queue_name] for queue_name in output_queues]
            if input_values is not None:
                init_params['input_values'] = input_values

            self._workers[worker_name] = []
            for i in range(number_of_instances):
                self._workers[worker_name].append(WorkerClass(**init_params))

    def _join_workers(self):
        for worker_name in self._workers:
            for worker_thread in self._workers[worker_name]:
                worker_thread.join()


    def process_pipeline(self):
        self._load_pipeline()
        self._initialize_queues()
        self._initialize_workers()
        self._join_workers()
