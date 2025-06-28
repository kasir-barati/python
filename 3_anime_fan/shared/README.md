# Celery Quick start

```py
from celery import Celery

app = Celery('tasks', broker='pyamqp://rabbitmq:123456@localhost//')

@app.task
def add(x, y):
    return x + y
```

- ### First argument to `Celery`:
  - The name of the current module.
  - This is only needed so that names can be automatically generated when the tasks are defined in the `__main__` module.
    - TBH I do not understand this part
- ### Second argument to `Celery`:
  - The broker keyword argument, specifying the URL of the message broker you want to use.
  - Here we are using RabbitMQ (**also the default option**). -
  - For RabbitMQ use `amqp://localhost`
  - For Redis use `redis://localhost`
- You defined a single task, called `add`, returning the sum of two numbers.
- # Running the Celery worker server
  - You can now run the worker by executing our program with the worker argument:
  - `celery -A tasks worker --loglevel=INFO`
    - `celery worker --help`
    - `celery --help`
  - In production you’ll wanna run the worker in the background as a daemon.
    - Use provided tools by your platform, or `supervisord`
- # Call our task
  - `delay()`
    - A handy shortcut to the `apply_async()` method that gives greater control of the task execution
      ```cmd
      $ python
      >>> from tasks import add
      >>> add.delay(4, 4)
      ```
  - Task has now been processed by the worker you started earlier.
  - It returns an `AsyncResult` instance.
    - Use it to:
      - Check the state of the task
      - Wait for the task to finish
      - Get its return value
      - Get the exception and traceback just in failure case
    - Results are not enabled by default.
      - To do:
        - Remote procedure calls
        - Keep track of task results in a database
      - You'll need to configure Celery to use a result backend.
        - Store or send the states somewhere.
        - There are several built-in result backends to choose from:
          - SQLAlchemy
          - Django ORM
          - MongoDB
          - Memcached
          - Redis
          - RPC (RabbitMQ/AMQP)
          - or your own backend.
      - [Learn more](https://docs.celeryq.dev/en/latest/userguide/tasks.html#task-result-backends)
    - RPC result backend:
      - Sends states back as transient messages.
- ### Third arguments to `Celery`:
  - The Backend
    ```py
    # In case you're using RabbitMQ as message broker
    app = Celery('tasks', broker='pyamqp://', backend='rpc://',)
    # In case you're using Redis as message broker
    app = Celery('tasks', backend='redis://localhost', broker='pyamqp://')
    ```
  - `result.ready()`
    - `ready()` returns whether the task has finished processing or not
      ```cmd
      $ python
      >>> from tasks import add
      >>> result = add.delay(4, 4)
      >>> result.ready()
      ```
  - `result.get(timeout=1)`
    - Get the result.
    - Based on my observation this code will turns async operation into a sync operation which I assume we do not want
    - `result.get(propagate=False)`
      - Calling `.get` twice raise an exception.
      - We change it via this argument
  - `result.traceback`
    - To get the error stack
  - ## :warning:**Backends use resources to store and transmit results**:warning:
    - Release resources by calling `get()` or `forget()` on **EVERY** `AsyncResult` instance returned after calling a task

# Configuration

- Like a consumer appliance, doesn’t need much configuration to operate.
- It has an input and an output.
  - The input must be connected to a broker
  - The output can be optionally connected to a result backend.
  - However, if you look closely at the back, there’s a lid revealing loads of sliders, dials, and buttons: this is the configuration.
    - ## **IDK what does this mean**
- Default configuration should be good enough for most use cases
- Setup conf:
  - Directly on the app
  - Use a dedicated configuration module.

# Using Celery with Django

- Define an instance of the Celery library (called an "app")
  - Create a file in `project_name/project_name/celery.py`
- Import this app in your `project_name/project_name/__init__.py` module.
  - App is loaded when Django starts so that the `@shared_task` decorator (mentioned later) will use it:
- # Calling Tasks
  - The API defines a standard set of execution options, as well as three methods:
    - `apply_async(args[, kwargs[, …]])`
      - Sends a task message.
    - `delay(*args, **kwargs)`
      - Shortcut to send a task message, but doesn’t support execution options.
    - `calling (__call__)`
      - `add(2, 2)`
      - Task will not be executed by a worker, but in the current process instead (a message won’t be sent).
  - Cheat sheet
    - `T.delay(arg, kwarg=value)`
      - Star arguments shortcut to `.apply_async`. (`.delay(*args, **kwargs)` calls .`apply_async(args, kwargs)`).
    - `T.apply_async((arg,), {'kwarg': value})`
    - `T.apply_async(countdown=10)`
      - executes in 10 seconds from now.
    - `T.apply_async(eta=now + timedelta(seconds=10))`
      - executes in 10 seconds from now, specified using eta
    - `T.apply_async(countdown=60, expires=120)`
      - executes in one minute from now, but expires after 2 minutes.
    - `T.apply_async(expires=now + timedelta(days=2))`
      - expires in 2 days, set using datetime.
- # Canvas: Designing Work-flows
  - ## We need to define tasks in a specific order, so we should use these tools
    - ### Signatures
      - A `signature()` wraps the arguments, keyword arguments, and execution options of a single task invocation in a way such that it can be passed to functions or even serialized and sent across the wire.
    - ### The Primitives
      - Here we need `chain` to chain tasks
      - Link together signatures so that one is called after the other
      - Essentially forming a chain of callbacks.
    - ### kombu.exceptions.EncodeError: Object of type TemporaryUploadedFile is not JSON serializable
      - When we create a celery task, it serializes the arguments so that it can store the message in the queue backend (RabbitMQ, Redis, etc).
      - The default serializer is JSON, and a binary file is not JSON-serializable.
      - We can `base64` encode the binary file to text
        - **But we do not do this**
          - The size of the data increases drastically
          - You'll be passing around potentially very large messages.
          - With lots of large messages, you'll eventually run out of memory/space in your backend, and it will make it hard to inspect or log messages.
      - Solution: Save the binary file somewhere, and pass a reference (filename, S3 URL, database key, etc) to the task.
        - I did this and I will just then convert the files to lower qualities
