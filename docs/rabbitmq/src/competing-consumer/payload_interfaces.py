"""Message payloads"""

from typing import TypedDict


class RegisteredUserPayload(TypedDict):
    """User data, published on registration"""

    id: str
    name: str
