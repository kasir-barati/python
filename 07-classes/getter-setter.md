# Getter & Setter

- Do not need to necessarily define them.
- **If** you **need them** you can **add them**.

> [!NOTE]
>
> **Jargon time:**
>
> - Getter: a method for getting the value of a data attribute.
> - Setter: a method for setting the value of a data attribute.

```py
class User:
    """ Create a user and determine their email provider """

    def __init__(self):
        self._email = ''
        self._email_provider = ''

    def _get_email(self) -> str:
        return self._email

    def _set_email(self, email: str) -> None:
        if email.endswith("@gmail.com"):
            self._email_provider = 'Google'
        elif email.endswith("@yahoo.com"):
            self._email_provider = 'Yahoo'
        else:
            self._email_provider = "unknown"

        self._email = email

    email = property(_get_email, _set_email)
```

- `property([fget=None, fset=None, fdel=None, doc=None])` function:

  - Defines properties.
  - A built-in function for creating and returning a property object.
    - **A class** with a function-like name.
  - Attach implicit _getter_ and _setter_ methods to given class attributes.
  - Python automatically calls the setter getter method when we try to assign a value to it or read from it respectively.

  | Argument | Description                                                        |
  | -------- | ------------------------------------------------------------------ |
  | `fget`   | The method that returns the value of the data attribute.           |
  | `fset`   | The method that allows you to set the value of the data attribute. |
  | `fdel`   | The method that defines how the data attribute handles deletion.   |
  | `doc`    | A string representing the property’s docstring.                    |

- `property()` function can be used as a decorator as well. Making it a supernova :star_struck:.

  ```py
  class User:
      """ Create a user and determine their email provider """
      def __init__(self):
          self._email = None
          self._email_provider = None
      @property
      def email(self) -> str:
          return self._email
      @email.setter
      def email(self, email: str) -> None:
          if email.endswith("@gmail.com"):
              self._email_provider = 'Google'
          elif email.endswith("@yahoo.com"):
              self._email_provider = 'Yahoo'
          else:
              self._email_provider = "unknown"
          self._email = email
      @email.deleter
      def email(self):
          del self._email
          del self._email_provider
      def print_me(self):
          if hasattr(self, '_email'):
              print(self._email, end='\t')
          if hasattr(self, '_email_provider'):
              print(self._email_provider, end='')
          print()
  u = User()
  u.email = 'asdasd@asdas.com'
  u.print_me()
  del u.email
  u.print_me()
  ```

## Ref

- [Python's `property()`: Add Managed Attributes to Your Classes](https://realpython.com/python-property/).
