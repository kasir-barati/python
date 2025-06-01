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
