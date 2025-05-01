# [`datetime` Module](https://docs.python.org/3/library/datetime.html)

## `date` Class

```py
import datetime
birthdate = datetime.date(2005, 1, 1) # Year, Month, Day
print(birthdate)
```

> [!TIP]
>
> When coding and developing modules in Python try to avoid giving the same name to a class as your module since it can be quite confusing. Like what you can see here, `datatime.datetime`!
>
> Learn more about naming conventions in Python [here](https://peps.python.org/pep-0008/#naming-conventions). This is supper important since if you pick a bad name it will be hard to change later and also it became a tech debt which its interest rate will grow over time.

- The returned value might uses the locale-settings of your system, but in some cases it might not. This makes your code less reliable, thus we must specify the locale to be safe.

  ```py
  from datetime import date
  import locale
  locale.setlocale(locale.LC_ALL, "")
  print(date(2004, 12, 20))
  ```

  **Caution**:

  - This should be done in the main file of your project and not in the modules.
  - The second parameter of [`setlocale`](https://docs.python.org/3/library/locale.html#locale.setlocale) is a string that specifies the locale to be used, e.g. `en_US.utf-8` or `de_DE.utf-8`.
    - Empty string means the default system locale.
  - The locale should be installed on your system otherwise your code will crash.

### [`strftime`](https://docs.python.org/3/library/datetime.html#datetime.date.strftime)

```py
from datetime import date
birthdate = date(2004, 12, 20)
print(birthdate.strftime("%Y.%m.%d"))  # 2004.12.20
print(f"{birthdate.year}.{birthdate.month}.{birthdate.day}")
```

- This method uses the locale settings of the system it is running on.

> [!INFO]
>
> You can thank C programmers who have the religious belief that you only get so many vowels in your lifetime; the more vowels they type, the sooner they will die. Yes, it is string-format-time, and strptime is string-parse-time. Why the methods were not simply named "time_to_string" and "time_from_string" like sensible people would do is beyond understanding.
>
> &mdash; [Ref](https://stackoverflow.com/questions/50066116/meaning-of-strf-in-strftime#comment87149446_50066116)

## Getting The Current Date & Time

<table>
<thead><tr>
<th><code>now</code></th>
<th><code>today</code></th>
<th><code>utcnow</code></th>
</tr></thead>
<tbody><tr><td>

```py
from datetime import datetime
print(datetime.now())
```

</td><td>

```py
from datetime import datetime
print(datetime.today())
```

</td><td>

```py
from datetime import datetime
print(datetime.utcnow())
```

</td></tr></tbody>
</table>

> [!NOTE]
>
> Python doc states that `date.now()` is the preferred approach compare to `date.today()` and `date.utcnow()` ([ref](https://docs.python.org/3/library/datetime.html#datetime.datetime.now)).

We can get the difference of times like this:

```py
from datetime import datetime
birthdate = datetime(2005, 1, 1)
today = datetime.today()
print(today - birthdate)
```

> [!CAUTION]
>
> You cannot add two dates together, it will crash your app, for adding you need to use [timedelta](#timedelta):
>
> ```py
> from datetime import date
> date1 = date(2004, 12, 31)
> date2 = date(2005, 1, 1)
> print(date1 + date2)
> ```

## [`timedelta`](https://docs.python.org/3/library/datetime.html#timedelta-objects)

```py
from datetime import date, timedelta
duration = timedelta(days=10)
opening_date = date(2025, 7, 20)
end_date = opening_date + duration
print(end_date)
```

**Note**: date object does not have a time component, meaning if we specify hour, it will be lost. E.g. `timedelta(days=10, hours=1)`. But increasing it to `24` will make it a whole day, so it will change the returned value.

## [`time`](https://docs.python.org/3/library/datetime.html#time-objects)

```py
from datetime import time
print(time(12, 30))
```

- A (local) time of day.
- Independent of any particular day.
- Subject to adjustment via a [`tzinfo`](https://docs.python.org/3/library/datetime.html#datetime.tzinfo) object.

> [!NOTE]
>
> You cannot subtract instances of times, i.e. the following code crashes:
>
> ```py
> from datetime import time
> print(time(12, 10) - time(12, 30))
> ```
>
> ```bash
> Traceback (most recent call last):
>   File "/home/kasir/projects/python/main.py", line 2, in <module>
>     print(time(12, 10) - time(12, 30))
>           ~~~~~~~~~~~~~^~~~~~~~~~~~~~
> TypeError: unsupported operand type(s) for -: 'datetime.time' and 'datetime.time'
> ```

### ISO 8601

- The standard way of representing date and time.
- The support for this is limited in Python version 3.11 and below.
- The format is:
  - `YYYY-MM-DDTHH:MM:SS.mmmmmm±HH:MM`.
  - `T` is the separator between date and time.

<table>
<thead>
<tr>
<th><code>isoformat</code></th>
<th><code>date.fromisoformat</code></th>
</tr>
</thead>
<tbody><tr><td>

```py
from datetime import datetime
print(datetime(2023, 1, 1).isoformat())
```

</td><td>

```py
from datetime import date
print(date.fromisoformat("2023-01-01"))
```

</td></tr></tbody>
</table>
