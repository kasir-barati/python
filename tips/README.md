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
