<details>
<summary>Typd dictionary</summary>

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
