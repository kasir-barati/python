class Tag(object):
    def __init__(self, name: str, content: str):
        self.start_tag = f"<{name}>"
        self.end_tag = f"</{name}>"
        self.content = content

    def __str__(self):
        return f"{self.start_tag}{self.content}{self.end_tag}"


class Doctype(Tag):
    def __init__(self):
        self.start_tag = "<!DOCTYPE html>"
        self.end_tag = ""
        self.content = ""


class Head(Tag):
    def __init__(self, title: str) -> None:
        super().__init__("head", "")
        self.title = Tag("title", title)

    def __str__(self):
        self.content = str(self.title)
        return super().__str__()


class Body(Tag):
    def __init__(self) -> None:
        super().__init__("body", "")
        self.elements: list[Tag] = []

    def add_element(self, element: Tag):
        self.elements.append(element)

    def __str__(self) -> str:
        for element in self.elements:
            self.content += str(element)
        return super().__str__()


class Html(Tag):
    def __init__(self, title: str) -> None:
        super().__init__("html", "")
        self._doctype = Doctype()
        self._head = Head(title)
        self._body = Body()

    def add_element(self, element: Tag):
        self._body.add_element(element)

    def __str__(self) -> str:
        self.content = str(self._head) + str(self._body)
        html_content = super().__str__()

        return f"{self._doctype}{html_content}"


class Aggregation_Html(Tag):
    def __init__(self, head: Head, body: Body) -> None:
        super().__init__("html", "")
        self._doctype = Doctype()
        self._head = head
        self._body = body

    def __str__(self) -> str:
        self.content = str(self._head) + str(self._body)
        html_content = super().__str__()

        return f"{self._doctype}{html_content}"


if __name__ == '__main__':
    body = Body()
    body.add_element(Tag("h2", "Who Am I?"))
    body.add_element(Tag("p", "I am a software developer"))
    body.add_element(Tag("h2", "Education"))
    body.add_element(Tag("p", "Bachelor of Science in Computer Science"))

    head = Head("Resume")

    html = Aggregation_Html(head, body)

    del html

    print(body)
