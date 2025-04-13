# [Dictionaries](https://docs.python.org/3.9/library/stdtypes.html#mapping-types-dict)

- Built-in data type.
- It is not a sequence.
- A set of key: value pairs.

  ![dict](./assets/dict.png)

- Indexed by keys.

  - The `key` is case-sensitive.
  - We use a `key` to get values from a dictionary.
  - They can be strings, numbers, tuples:

    ```py
    info = {
        "name": "Claudius Ptolemy",
        100: ["Mathematician", "Astrologist", "Geologist"],
        ("Alexandria", "Egypt", "Roman Empire"): "Alexandria is the second largest city in Egypt and the largest city on the Mediterranean coast."
    }
    ```

    > [!CAUTION]
    >
    > If a tuple contains any mutable object either directly or indirectly, it cannot be used as a key.

  - **They have to be unique** within one dictionary.

## Get a Value

- `get` method:

  ```py
  car = {
    "name": "BYD",
    "model_number": 123,
    "plaque_number": "px123"
  }
  print(car.get("name"))
  ```

- Key as index:

  ```py
  print(car['name'])
  ```

> [!TIP]
>
> - `get` will return `None` when it cannot find a value for the provided key whereas the key as index approach will raise an exception in case it did not find it in the dictionary.
> - Key as index is faster than `get` method.
> - Sometimes we want our app to crash if the key was not present.
>
> ```py
> profile = {
>     "username": "Genghis_khan"
> }
> print(profile["age"])  # raises an exception
> print(profile.get("age"))  # returns None
> ```

- Get all keys like this:
  ```py
  info = {
      "name": "Claudius Ptolemy",
      "fields": ["Mathematician", "Astrologist", "Geologist"],
      "home_town": "Alexandria is the second largest city in Egypt and the largest city on the Mediterranean coast.",
      "died": 100
  }
  keys = list(info)
  sorted_keys = sorted(info)
  print(keys, sorted_keys)
  ```

## Delete a key-value Pair

- You can use `del`:

  ```py
  me = {"test": 123}
  del me["test"]
  print(me)  # {}
  ```

- You can also use `pop`, note that this method returns the value of the deleted key:

  ```py
  car.pop("name")
  ```

  And you can also specify a default value in case it did not exists in the dictionary.

  ```py
  car.pop("mileage", 0)  # 0 will be returned if "mileage" does not exist in the car dictionary
  ```

  Note that `pop` works in LIFO (Last In First Out). BTW we have another method which returns both key and value for that key called `popitem`.

> [!TIP]
>
> `del` performs better than `pop`.

## `in` Operator -- Membership Test Operator

- In dictionaries the `in` operator looks up for the keys:

  ```py
  if "production_date" in car:
      print(car['production_date'])
  ```

> [!NOTE]
>
> The `in` operator in a sequence (e.g. an array) looks for that value's presence in the sequence.
>
> ```py
> names = ["Mohammad", "Jawad"]
> if "Alex" in names:
>     print("Alex exists in the list")
> ```

## Loop Over a Dictionary

- You by default iterate over the keys:

  ```py
  for key in car:
      print(key)
      print(car[key])  # This is how you can get the values
  ```

- `items` method:

  ```py
  for key, value in car.items():  # Unpacking
      print(key)
      print(value)
  ```

> [!TIP]
>
> - The `items` method is more readable.
> - The `items` method is more efficient.

## Convert a List to Dictionary

- `enumerate` function:

  ```py
  arr = ["asd"]

  for key, val in enumerate(arr):
      print(key, val)
  ```

- Build dictionary directly from sequences of key-value pairs with the `dict()` constructor:

  ```py
  ai_figures = [("John McCarthy", 2011), ("Kate Crawford", None)]
  print(dict(ai_figures))
  # Yet another way:
  print(dict(key1="value1", key2="value2"))
  ```

## Dictionary Comprehensions

```py
numbers = {number: "even" if number % 2 == 0 else "odd"
           for number in range(1, 100)}
print(numbers)
```

## `setdefault` Method

Instead of

```py
account = {
    "credit": 123
}


def top_up(account):
    # TODO copy the object first
    if "credit" not in account:
        account["credit"] = 0

    account["credit"] += 10

    return account
```

You can do this:

```py
# ...
account["credit"] = account.setdefault("credit", 0) + 10
return account
```

## `update` Method

You can add key-value pairs of one dictionary to another by using this method:

```py
user = { "name": "jawad" }
account = { "IBAN": "DE123456789012" }
user.update(account)

print(user)
```

## Shallow Copy VS Deep Copy

- `copy` method does a shallow copy.

  ```py
  user1 = {"schools": ["zoom"]}
  user2 = user1  # user2 = user1.copy()
  user2["schools"].append("elder")
  print(user1)
  print(user2)
  ```

  So basically these two objects are pointing to the same address of memory. It copies references and not the things it is referring to.

- `deepcopy` helper function in `copy` module:

  ```py
  from copy import deepcopy
  user2 = deepcopy(user1)
  ```

> [!TIP]
>
> A simple deep copy helper function:
>
> ```py
> def simple_deepcopy(obj):
>     res = {}
>
>     for key, value in object.items():
>         if value is Array:
>             res[key] = value.copy()
>             continue
>
>         res[key] = value
>     return res
> ```

## `fromkeys` Method

- Creates a new dictionary from the given list.

## YouTube/Aparat

- [https://youtu.be/-QperLIB4b8](https://youtu.be/-QperLIB4b8).
- [https://aparat.com/v/jhdj52n](https://aparat.com/v/jhdj52n).

## Ref

- [5. Data Structures](https://docs.python.org/3/tutorial/datastructures.html).
