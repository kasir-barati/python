# Hot Reload

- To hot reload your Python script in dev env you need to install [`watchdog` library](https://pypi.org/project/watchdog/).
- I intentionally used `asyncio` and created [`dev_runner.py`](./src/dev_runner.py) to show how you can prevent seeing logs like this in your terminal whenever it hot reloads your app:

  ```cmd
  $ make start
  . .venv/bin/activate
  watchmedo auto-restart \
          --directory=./src \
          --pattern="*.py" \
          --recursive \
          -- python src/main.py
  main
  📍 s() called at 12:03:47
  📍 r() called at 12:03:47
  Traceback (most recent call last):
  File "/usr/lib/python3.12/asyncio/runners.py", line 118, in run
      return self._loop.run_until_complete(task)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/asyncio/base_events.py", line 687, in run_until_complete
      return future.result()
          ^^^^^^^^^^^^^^^
  File "/home/mjb/projects/python/docs/hot-reload/src/main.py", line 10, in main
      s()
      ^^^^
  asyncio.exceptions.CancelledError

  During handling of the above exception, another exception occurred:

  Traceback (most recent call last):
  File "/home/mjb/projects/python/docs/hot-reload/src/main.py", line 12, in <module>
      await asyncio.Future()
  ^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/asyncio/runners.py", line 194, in run
      return runner.run(main)
          ^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/asyncio/runners.py", line 123, in run
      raise KeyboardInterrupt()
  KeyboardInterrupt
  main
  📍 s() called at 12:03:57
  📍 r() called at 12:03:57
  ```
