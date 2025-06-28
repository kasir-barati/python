"""Message payloads"""

from typing import TypedDict


class UserCreatedPayload(TypedDict):
    """User data, published on registration"""

    id: str
    name: str
