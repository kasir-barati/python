# Custom Scalar Type

In a custom scalar type you can valdiate, and sanatize the data.

> [!NOTE]
>
> This is a contrived example. I mean we can do this way easier without having to create a new `NonEmptyTrimmedString` scalr type.

```py
from __future__ import annotations

from typing import Any, NewType

import strawberry


NonEmptyTrimmedString = NewType("NonEmptyTrimmedString", str)
"""
Non-empty, whitespace-trimmed string.
"""


def _parse_non_empty_trimmed_string(value: Any) -> str:
    if not isinstance(value, str):
        raise TypeError("NonEmptyTrimmedString must be a string")

    stripped = value.strip()

    if not stripped:
        raise ValueError("NonEmptyTrimmedString must not be empty or whitespace-only")

    return stripped


_NON_EMPTY_TRIMMED_STRING = strawberry.scalar(
    name="NonEmptyTrimmedString",
    description=(
        "String scalar that trims leading/trailing whitespace and rejects "
        "empty or whitespace-only values."
    ),
    serialize=lambda value: value,
    parse_value=_parse_non_empty_trimmed_string,
)


SCALAR_MAP: dict[object, Any] = {
    NonEmptyTrimmedString: _NON_EMPTY_TRIMMED_STRING,
}
"""
The full scalar map to hand to :class:`StrawberryConfig` when building the schema.
"""

```

> [!TIP]
>
> This can be even simplified further:
> ```py
> from typing import Annotated
> from pydantic import StringConstraints
>
> NonEmptyTrimmedString = Annotated[
>     str,
>     StringConstraints(strip_whitespace=True, min_length=1),
> ]
>
> TtsText = Annotated[
>     str,
>     StringConstraints(strip_whitespace=True, min_length=1, max_length=4000),
> ]
>
> WordInputText = Annotated[
>     str,
>     StringConstraints(strip_whitespace=True, min_length=1, max_length=100),
> ]
> ```
>
> &mdash; Ref: https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.StringConstraints
