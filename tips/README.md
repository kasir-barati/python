- [Thread-Safe Singleton Pattern in Python](https://github.com/xbeat/Machine-Learning/blob/main/Thread-Safe%20Singleton%20Pattern%20in%20Python.md).
  - Example: [./examples/thread-safe-singleton-pattern.py](./examples/thread-safe-singleton-pattern.py).
- [Retry helper function](./examples/retry.py).

<details>
<summary>Change the return type based on a parameter in Python</summary>

```py
from typing import overload, Literal, Any, TypedDict


class User(TypedDict):
    id: str
    name: str


class UserRepository:
    @overload
    def update_user(
        self, filters: Any, return_update_users: Literal[True]
    ) -> list[User]: ...
    @overload
    def update_user(
        self, filters: Any, return_update_users: Literal[False]
    ) -> None: ...
    def update_user(self, filters: Any, return_update_users: bool) -> list[User] | None:
        # TODO: update users!

        if not return_update_users:
            return

        # ...
        return []


userRepository = UserRepository()
users = userRepository.update_user({}, True)
result = userRepository.update_user({}, False)

# Verify the types and values
print(f"users: {users}, type: {type(users)}")
print(f"result: {result}, type: {type(result)}")
```

</details>

<details>
<summary>Function overloading in Python</summary>

```py
import base64
import numpy
import requests
from typing import overload

@overload
def get_as_base64(imageOrUrl: numpy.ndarray) -> str: ...
@overload
def get_as_base64(imageOrUrl) -> str: ...
def get_as_base64(imageOrUrl: str | numpy.ndarray) -> str:
    if isinstance(imageOrUrl, numpy.ndarray):
        image_bytes = imageOrUrl.tobytes()
        return base64.b64encode(image_bytes).decode("utf-8")

    return base64.b64encode(requests.get(imageOrUrl).content).decode("utf-8")
```

And here is its unit test:

```py
from numpy import arange, uint8
from unittest.mock import MagicMock, Mock, patch

from .get_as_base64 import get_as_base64

def test_get_as_base64_with_numpy_ndarray():
    image = arange(6, dtype=uint8).reshape((2, 3))
    expected = "AAECAwQF"

    result = get_as_base64(image)

    assert result == expected

@patch("requests.get")
def test_get_as_base64_with_uri(mock_get: MagicMock):
    fake_image_bytes = b"image in binary"
    mock_response = Mock()
    mock_response.content = fake_image_bytes
    mock_get.return_value = mock_response
    url = "http://localhost/some/file.png"
    expected = "aW1hZ2UgaW4gYmluYXJ5"

    result = get_as_base64(url)

    assert result == expected
    mock_get.assert_called_once_with(url)
```

</details>

<details>
<summary>Struct in Python</summary>

bundling together a few named data items. The idiomatic approach is to use dataclasses for this purpose:

```py
from dataclasses import dataclass


@dataclass
class Employee:
    name: str
    salary: int
    department: str

john = Employee('john', 'computer lab', 1000)
print(john.department)
```

</details>

<details>
<summary>Typed dictionary</summary>

```py
from typing import TypedDict


class Person(TypedDict):
    age: int

person: Person = {
    'age': 22
}
```

</details>

<details>
<summary>Abstract class</summary>

```py
from abc import ABC


class Person(ABC):
    age: int

def me(user: Person) -> None:
    print(user.age)
```

</details>

<details>
<summary>Casting types/Type assertion</summary>

This is simalr to what you can do with `as` in Typescript.

```py
from typing import cast
from enum import Enum


class AdminRole(Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    ADMIN = "ADMIN"


class Role(Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    ADMIN = "ADMIN"
    USER = "USER"


def create_product(role: Role) -> None:
    print(role)


create_product(cast(Role, AdminRole.ADMIN))
```

</details>
