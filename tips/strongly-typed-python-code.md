# Type Hinting Techniques in Python

I love to have types, because they gimme a sense of what the heck am I doing and what I should not probably do :grin:.

<details>
<summary>How to define an interface which will accept any class as long as it has field x of type y?</summary>

```py
from typing import Protocol, Any
class EventPayload(Protocol):
    id: str
    body: Any
    # ...
```

</details>

<details>
<summary>How to annotate tuple of tuples?</summary>

The `...` (ellipsis) means it can have any number of these inner tuples (including zero).

```py
metadata: tuple[tuple[str, str], ...] = (
    ("request-id", "83c5952d-ce66-4c1b-97cd-d732983e9cf5"),
    ("authorization", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWUsImlhdCI6MTUxNjIzOTAyMn0.KMUFsIDTnFmyG3nMiGM6H9FNFUROf3wh7SmqJp-QV30"),
)
```

</details>

<details>
<summary>Change the return type based on a parameter in Python</summary>
<table>
<thead><tr><th>No default value</th><th>With default value</th></tr></thead>
<tbody><tr><td>

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
    def update_user(
        self, filters: Any, return_update_users: bool
    ) -> list[User] | None:
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

</td><td>

```py
from typing import overload, Literal, Any, TypedDict


class User(TypedDict):
    id: str
    name: str


class UserRepository:
    @overload
    def update_user(
        self, filters: Any, return_update_users: Literal[True] = True
    ) -> list[User]: ...
    @overload
    def update_user(
        self, filters: Any, return_update_users: Literal[False]
    ) -> None: ...
    def update_user(
        self, filters: Any, return_update_users: bool = True
    ) -> list[User] | None:
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

</td></tr></tbody>
</table></details>

<details>
<summary>Having a generic base class which can be extended</summary>

Assume you wanna have same message payload structure. So what you need is something like this:

- All messages should have `body` which is dependent on each message. So it is the generic part which can change for each message. But inside the body you have to have e.g. `timestamp` which represents when it was sent.
- You have also a common field called `metadata` which will always look the same.

```py
from typing import Generic, TypeVar

from typing_extensions import TypedDict


# Define a base TypedDict for the required 'timestamp' field
class RabbitmqMessageBody(TypedDict):
    timestamp: str
    # ...


# Create a generic TypeVar for custom message bodies
Body = TypeVar("Body", bound=TypedDict)


class RabbitmqMessageMetadata(TypedDict):
    retry: int
    # ...


# Define the main RabbitmqMessage as a generic TypedDict
class RabbitmqMessage(TypedDict, Generic[Body]):
    body: Body  # Body must include fields in RabbitmqMessageBody
    metadata: RabbitmqMessageMetadata


# Define your specific message body
class UserCreatedMessage(RabbitmqMessageBody):  # Inherits shared_field
    id: str


# Create an instance that satisfies the structure
something: RabbitmqMessage[UserCreatedMessage] = {
    "body": {
        "id": "",
        "timestamp": "",
    },
    "metadata": {"retry": 2},
}
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
