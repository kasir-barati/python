# Super

- In Python, the `super()` function is used to call a method from a parent class.

  ```py
  class Person(object):
      def __init__(self, name: str, age: int) -> None:
          self.name = name
          self.age = age
  class Employee(Person):
      def __init__(self, name: str) -> None:
          super(Employee, self).init(name, 20)
          # super().__init__(name, 20)
          # Person.__init__(self, name, 20)
  ```

# Override Methods

- We can override methods in subclasses.

  ```py
  class Eagle(FlyingBird):
      # ...
      def eat(self) -> str:
          if not hasattr(self, 'prey_name'):
              return "No prey found. Cannot eat."

          msg = super().eat()
          msg += f" It's meal is a ${self.prey_name}"

          return msg
  ```

- You can see that we are first calling the parent class's `eat()` method and then adding our own logic.
- This way we can extend the parent class's functionality without having to change the parent class.

# Composition

- A technique for building complex objects by combining simple objects.
  - Simple objects will not be exposed outside of the composed object.
  - So you have an API to work with without having to worry about which object is being used internally.

> [!TIP]
>
> **Is a..**, and **Has a..**:
>
> - **Is a..** is about inheritance. E.g. duck _is a_ bird. So we can use inheritance to model this relationship.
> - **Has a..** is about composition. E.g. duck _has a_ beak. So we can use composition to model this relationship.

```py
class Wing:

    def __init__(self, length: int) -> None:
        self.length = length

class Duck:

    def __init__(self, name: str) -> None:
        self.name = name
        self.wing = Wing(10)

    def swim(self) -> None:
        print(f"{self.name} is swimming.")

    def walk(self) -> None:
        print(f"{self.name} is walking.")

    def fly(self) -> None:
        print(f"{self.name} is flying because of its wing length of {self.wing.length}.")

class Penguin:

    def __init__(self, name: str) -> None:
        self.name = name

    def swim(self) -> None:
        print(f"{self.name} is swimming.")

    def walk(self) -> None:
        print(f"{self.name} is walking.")
```

## HTML & Composition

A HTML document is a composition of ([ref](https://html.spec.whatwg.org/multipage/introduction.html#a-quick-introduction-to-html)):

- Document type declaration.
- `html` tag.
- `head` tag.
- `body` tag.

```py
class Tag(object):

    def __init__(self, name: str, content: str) -> None:
        self.start_tag = f"<{name}>"
        self.end_tag = f"</{name}>"
        self.content = content

    def __str__(self) -> str:
        return f"{self.start_tag}{self.content}{self.end_tag}"


class DocType(Tag):

    def __init__(self) -> None:
        super().__init__("!DOCTYPE html", '')
        # DOCTYPE doesn't have an end tag and content
        del self.end_tag
        del self.content


class Head(Tag):

    def __init__(self, title: str) -> None:
        super().__init__("head", '')
        self.content = str(Tag("title", title))


class Body(Tag):

    def __init__(self) -> None:
        super().__init__("body", "")
        self._body_contents: list[Tag] = []

    def append(self, tag: str, content: str) -> None:
        self._body_contents.append(Tag(tag, content))

    def __str__(self) -> str:
        for tag in self._body_contents:
            self.content += str(tag)

        return super().__str__()


class Html(object):
    def __init__(self, document_title: str) -> None:
        super().__init__("html", "")
        self._head = Head(document_title)
        self._body = Body()

    def append(self, tag: str, content: str) -> None:
        self._body.append(tag, content)

    def __str__(self) -> str:
        content = str(self._head)
        content += str(self._body)
        self.content = content
        return super().__str__()


if __name__ == "__main__":
    html = Html("My Document")
    html.append("h1", "Heading")
    html.append("p", "This is a paragraph.")
    print(html)
```

### Composition Live Coding Example

You can see the code [here](./assets/composition-live-coding-example.py).

# Aggregation

- Weak form of composition.
- Aggregation is a form of association where two objects are loosely coupled.
- If you delete the container object, the contained object will continue to exist.

<table>
<thead><tr><th>First version</th><th>Modified Class</th></tr></thead>
<tbody>

<tr><td>

```py
html = Html("My Document")
body = Body()
body.append("h1", "Heading")
body.append("p", "This is a paragraph.")
html._body = body
print(html)
print()
del html
print(body)
```

</td><td>

```py
class Html(object):
    def __init__(self, doc_type: DocType, head: Head, body: Body) -> None:
        self._doc_type = doc_type
        self._head = head
        self._body = body
```

This is how you should modify the `Html` class to make it work with aggregation technique, but in the first version we do not have to change the `Html` class implementation.

</td></tr>
</tbody>
</table>

> [!TIP]
>
> When to use composition and when to use aggregation?
>
> - In this example we do not need to change the `doc_type` and `head` objects, so we can use composition.
> - But we need to change the content of the `body` object often (user clicks on something and we need to swap something with something else), so in this scenario we can utilize aggregation to make the code more flexible.

## YouTube/Aparat

- [https://youtu.be/q3r_DQ5fgOk](https://youtu.be/q3r_DQ5fgOk).
- [https://aparat.com/v/oqy8t19](https://aparat.com/v/oqy8t19).

# [`repr`](https://docs.python.org/3/library/functions.html#repr)

- Printable representation of an object.
- We can have a dunder method for this one:

  ```py
  class Person:
      def __init__(self, name, age):
          self.name = name
          self.age = age

      def __repr__(self):
          return f"Person('{self.name}', {self.age})"
  ```
