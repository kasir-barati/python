# Generators

- Creates iterators.
- Written like regular functions but use the `yield` statement whenever they want to return data.
- Each time [`next()`](#next) is called on it, the generator resumes where it left off (it remembers all the data values and which statement was last executed).
  - The local variables and execution state are automatically saved between calls.
  - Easier to write, and much more clear than an approach using instance variables like `self.index` and `self.data` when we wanna iterate over attributes in a class.

> [!NOTE]
>
> Generators when terminating, automatically raise `StopIteration`.

## [`next`](https://docs.python.org/3/library/functions.html#next)

- Retrieve the next item from the iterator by calling its [`__next__`](../07-classes/dunder-methods.md#__iter__--__next__) method.

```py
from typing import Iterator


def reverse(data: str) -> Iterator[str]:
    for index in range(len(data)-1, -1, -1):
        yield data[index]

for char in reverse('golf'):
    print(char)
```

## [Generator Expressions](https://peps.python.org/pep-0289/)

- Simple generators can be coded succinctly as expressions using a syntax similar to list comprehensions.
- Useful when the generator is used right away by an enclosing function.
  - Especially useful with functions like `sum()`, `min()`, and `max()` that reduce an iterable input to a single value.
- More compact but less versatile than full generator definitions.
- Tend to be more memory friendly than equivalent list comprehensions.

```py
print(sum(i*i for i in range(10)))
```

## YouTube/Aparat

- [https://youtu.be/\_LOyg2cXfkQ](https://youtu.be/_LOyg2cXfkQ).
- [https://aparat.com/v/wvye470](https://aparat.com/v/wvye470).
