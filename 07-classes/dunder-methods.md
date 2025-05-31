# Dunder Methods

- Magic methods.
- Special methods in Python that are surrounded by double underscores.
- are not meant to be invoked directly by the user but are internally invoked by the Python interpreter to perform specific actions.

  <details>
  <summary>E.g. when you wanna specify how two objects should be added together, you can define a <code>__add__</code> method for your classes.</summary>

  ```py
  class Account:
    def __init__(self, balance: float):
        self.balance = balance
  class Credit:
      def __init__(self, amount: float):
          self.amount = amount
      def __add__(self, account: Account) -> float:
          return account.balance + self.amount
  my_account = Account(100)
  my_credit = Credit(20)
  print(my_credit + my_account)
  ```

  </details>

## [`__init__`](https://docs.python.org/3/reference/datamodel.html#object.__init__)

- The constructor method.
- Called when an object is instantiated.
- Used to initialize the object's attributes.
- Will be used for things like performing any necessary setup or initialization tasks as well.

```py
class Animal:
    """
    Create an animal

    Attributes:
        name: The name of the animal.
        species: The species of the animal.
    """

    def __init__(self, name: str, species: str):
        self.name = name
        self.species = species
```

> [!TIP]
>
> In python we have in fact two method which will be called when an object is instantiated, [`__new__`](https://docs.python.org/3/reference/datamodel.html#object.__new__) and `__init__`. `__new__` is called first and it's responsible for creating the object, while `__init__` is called second and it's responsible for initializing the object.

## [`__str__`](https://docs.python.org/3/reference/datamodel.html#object.__str__)

- The string representation of an object.
- Used to provide a human-readable string representation of an object.

```py
class BankAccount:
    """
    Create a bank account

    Attributes:
        account_number: The account number.
        balance: The balance of the account.
    """

    def __init__(self, account_number: int, balance: float):
        self.account_number = account_number
        self.balance = balance

    def __str__(self):
        return f"Account Number: {self.account_number}, Balance: {self.balance}"

my_account = BankAccount(123456789, 1000.0)
print(my_account)
```

## YouTube/Aparat

- [https://youtu.be/Po_2bCv8_uc](https://youtu.be/Po_2bCv8_uc).
- [https://aparat.com/v/fxld834](https://aparat.com/v/fxld834).

## [`__iter__`](https://docs.python.org/3/library/stdtypes.html#container.__iter__) & [`__next__`](https://docs.python.org/3/library/stdtypes.html#iterator.__next__)

If you need to loop over your class and wanted to define how it should do it you need to implement `__iter__` and `__next__`.

<table>
<thead><tr><th>Not a Good Solution</th><th><a href="../09-generators/README.md">Generators</a></th><th><code>__iter__</code> & <code>__next__</code></th></tr></thead>
<tbody><tr><td>

```py
class Person(object):
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
        self._data_attributes = ["name", "age"]

    def __iter__(self):
        return self

    def __next__(self):
        if len(self._data_attributes) == 0:
            raise StopIteration

        return getattr(self, self._data_attributes.pop(0))


p1 = Person("John", 30)

for i in p1:
    print(i)
```

**Note**, this solution is modifying `_data_attributes` during iteration (using `pop(0)`), which ain't good practice since we might want to use it somewhere else in that class.

</td><td>

```py
from typing import Iterator


class Person(object):
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
        self._data_attributes = ["name", "age"]

    def __iter__(self) -> Iterator[str | int]:
        # return (getattr(self, attr) for attr in self._data_attributes)
        for attr_name in self._data_attributes:
            yield getattr(self, attr_name)
```

</td><td>

```py
class Person(object):
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
        self._data_attributes = ["name", "age"]
        self._index = 0  # Track iteration state

    def __iter__(self):
        self._index = 0  # Reset for new iterations
        return self

    def __next__(self):
        if self._index >= len(self._data_attributes):
            raise StopIteration
        attr_name = self._data_attributes[self._index]
        self._index += 1
        return getattr(self, attr_name)
```

</td></tr></tbody>
</table>

> [!TIP]
>
> If you need to define how you're `dataclass` should be converted to a dictionary you can use `__iter__` method, this is similar to `__str__` method:
>
> ```py
> from dataclasses import dataclass
> 
> 
> @dataclass
> class User:
>     def __init__(self):
>         self.name = "something"
>         self.age = 123
>
>     def __iter__(self):
>         yield "name", self.name
>         yield "age", self.age
>
> temp = User()
> print(dict(temp))
> ```
