# [`zoneinfo` Module](https://docs.python.org/3/library/zoneinfo.html).

- This is a new module added in Python 3.9. Thus if you wanna be able to run your program with Pythons below 3.9, you need to import it conditionally:

  ```py
  try:
    import zoneinfo
  except ImportError:
    from backports import zoneinfo
  ```

  This might show you an error in your IDE, but it's fine. It will work just fine depending on your Python version.

- We can get the time in different timezones like this:

  ```py
  from datetime import timezone, datetime
  from zoneinfo import ZoneInfo
  utc_now = datetime.now(timezone.utc)
  print(f'Now in UTC: \t\t\t {utc_now}')
  print(f'Now in your local timezone: \t {datetime.astimezone(utc_now)}')
  singapore_timezone = ZoneInfo('Asia/Singapore')
  print(f'Now in Singapore timezone: \t {datetime.now(singapore_timezone)}')
  ```

- Print the available timezones:

  ```py
  from zoneinfo import available_timezones
  print('\n'.join(available_timezones()))
  ```
