# Unpacking objects in Python

- Order matters!
- In JavaScript we call this destructuring objects.
- To skip a value, use a placeholder variable (commonly an underscore `_`)

```py
person = {
    'name': 'Alice',
    'age': 30,
    'city': 'New York'
}

name, age, city = person.values()
print(f"{name=}, {age=}, {city=}")
# Output: name='Alice', age=30, city='New York'

age, city, name = person.values()
print(f"{name=}, {age=}, {city=}")
# Output: name='New York', age='Alice', city=30

_, age, city = person.values()
print(f"{age=}, {city=}")
# Output: age=30, city='New York'
```
