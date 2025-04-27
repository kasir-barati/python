# Usage of `repr` Function

```py
class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def __repr__(self):
        return f"I am '{self.name}', {self.age} years old."


print(repr(Person("Yu", 123)))
```

- [Ref](https://docs.python.org/3/library/functions.html#repr).

# Match Statement for Classes

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def where_is(point):
    match point:
        case Point(x=0, y=0):
            print("Origin")
        case Point(x=0, y=y):
            print(f"Y={y}")
        case Point(x=x, y=0):
            print(f"X={x}")
        case Point():
            print("Somewhere else")
        case _:
            print("Not a point")

where_is((1, 2)) # "Not a point"
where_is(Point(1, 2)) # "Somewhere else"
where_is(Point(0, 0)) # "Origin"

var = 2
where_is(Point(1, var))
# Equivalent syntaxes:
#   - Point(1, y=var)
#   - Point(x=1, y=var)
#   - Point(y=var, x=1)
```

> A recommended way to read patterns is to look at them as an extended form of what you would put on the left of an assignment, to understand which variables would be set to what. Only the standalone names (like var above) are assigned to by a match statement. Dotted names (like foo.bar), attribute names (the x= and y= above) or class names (recognized by the “(…)” next to them like Point above) are never assigned to.

This explanation is related to Python's structural pattern matching, introduced in **PEP 634** (Python 3.10+). Let's break down the statement with examples:

### **Key Insight:**

- **Standalone Names** are assigned values.
- **Dotted Names, Attributes, and Class Names** are only matched against but never assigned to.

---

### **Example 1: Standalone Names Get Assigned**

```python
point = (3, 4)

match point:
    case (x, y):  # Standalone names
        print(f"x: {x}, y: {y}")
```

**Explanation:**

- `x` and `y` are **standalone names**, so they are assigned the values `3` and `4` respectively.

---

### **Example 2: Dotted Names Are Matched, Not Assigned**

```python
import math

value = math.pi

match value:
    case math.pi:  # Dotted name
        print("Matched pi")
```

**Explanation:**

- `math.pi` is a **dotted name**; Python **matches** the value `math.pi` rather than assigning it. If `value` was something else, the match would fail.

---

### **Example 3: Class Names Are Matched, Not Assigned**

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(1, 2)

match p:
    case Point(x, y):  # Class name matching
        print(f"x: {x}, y: {y}")
```

**Explanation:**

- `Point(x, y)` matches the instance `p`. If `p` is an instance of `Point`, its attributes `x` and `y` are extracted into standalone variables `x` and `y`.

---

### **Example 4: Attribute Names Are Matched, Not Assigned**

```python
data = {"x": 10, "y": 20}

match data:
    case {"x": x_val, "y": y_val}:  # Standalone names assigned
        print(f"x: {x_val}, y: {y_val}")

    case {"x": 10, "y": 20}:  # Exact value match, no assignment
        print("Exact match")
```

**Explanation:**

- In the first case, `x_val` and `y_val` are **standalone names**, so they are **assigned**.
- In the second case, `{"x": 10, "y": 20}` **matches the values** directly, not assigning anything.

---

### Summary:

1. **Standalone names** (like `x` and `y`) get **assigned** values.
2. **Dotted names**, **attribute names**, and **class names** are **matched** but **not assigned**.

Would you like deeper examples or more specific pattern-matching cases?

---

# Enums and `match` Statement

- Named constants: predefined, immutable values.
- Use dotted names to prevent named constants from being interpreted as capture variable:
  - Scoped within the `Color` enum and not confused with local variables or other identifiers in the code.

```python
from enum import Enum
class Color(Enum):
    RED = 'red'
    GREEN = 'green'
    BLUE = 'blue'

color = Color(input("Enter your choice of 'red', 'blue' or 'green': "))

match color:
    case Color.RED:
        print("I see red!")
    case Color.GREEN:
        print("Grass is green")
    case Color.BLUE:
        print("I'm feeling the blues :(")
```

# Custom Exceptions

https://docs.python.org/3/tutorial/errors.html#user-defined-exceptions

# Exception and Inheritance

```py
class B(Exception):
    pass
class C(B):
    pass
try:
    raise B()
except C:
    print("C")
except B:
    print("B")
```

- Here you might think that when we say `raise C()` it will be caught by the first `except` but that's not how Python works. It will be handled by the `except B` block.
- But if we reverse the order of `except` blocks and `raise C()` it will logs `B`. This is because `C` derives from `B`, thus catchable by `except B`:
  ```py
  try:
      raise C()
  except B:
      print("B")
  except C:
      print("C")
  ```
- You can make sense of it with your knowledge about inheritance and this visualization:

  ![Inheritance hierarchy between B, C, and D](./exception-inheritance.png)
