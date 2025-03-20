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
