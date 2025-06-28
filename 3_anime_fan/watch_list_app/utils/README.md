# next function

- Retrieve the next item from the iterator by calling its `__next__()` method.
  ```py
  list1 = [1, 2, 3, 4, 5]
  # converting list to iterator
  list1 = iter(list1)
  print("The contents of list are : ")
  # printing using next()
  # using default
  while True:
      val = next(list1, 'end')
      if val == 'end':
          print('list end')
          break
      else:
          print(val)
  ```

# Comparison with None

- Comparisons to singletons like None should always be done with is or is not, never the equality operators.
- [Stackoverflow Q&A](https://stackoverflow.com/questions/3965104)

# `os.path.*`

- Some useful functions on pathnames
- Unlike a unix shell, Python does not do any automatic path expansions.
- methods:
  - `os.path.dirname`
    - Returns the directory of the given file path.
  - `os.path.basename`
    - To get the file name from a complete path
  - `os.path.isabs`
    - To check if a path is absolute or not
  - `os.path.splitext`
    - To separate filename from its extension
    - Not too accurate, I mean `abc.tar.gz` will be splited into `('abc.tar', '.gz')`

# Handling CPU intensive tasks in a Django webapp

- We won't wanna force the client to wait for a response.
  - I meant the converting uploaded video into multiple low quality
- Do the tasks in background process.
  - Notify client via web sockets, or just store the results in the database
  - Do not run tasks simultaneously when multiple concurrent user send request
  - Queue tasks and automatically runs them in an optimal way
    - Based on number of cores
    - Available memory
    - Based on users who are currently online.
    - etc
  - Design your database drastically good
  - Develop efficient algorithms.
- refs:
  - [stackoverflow](https://stackoverflow.com/questions/25750764)
- ## [Celery](https://docs.celeryq.dev/en/latest/getting-started/first-steps-with-celery.html)
  - Simple, flexible, reliable distributed system.
  - **Batteries included**
  - Less learning curve
  - Scalable
  - A task queue with focus on real-time processing
  - Supports task scheduling
  - ### Steps to use it:
    - Choosing a message broker:
      - We need a solution to send and receive messages
      - Available choices:
        - RabbitMQ:
          - Feature-complete, stable, durable and easy to install.
          - It’s an excellent choice for a production environment.
          - `docker pull rabbitmq:3.9.20-management-alpine`
            - Keep to specific versions
            - Use alpine to prevent running out of storage
        - Redis:
          - Feature-complete
          - **But** more susceptible to data loss in the event of abrupt termination or power failures.
          - `docker pull redis:7.0.2-alpine3.16`
        - And some other less known options which I ignore them deliberately :smile:
      - After choosing message broker we do install celery:
        - `pip install celery`
      - Instantiate one celery
        - We call IT **Celery application** OR **app**
        - Entry-point, so it must be possible for other modules to import it.
