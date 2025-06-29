from typing import TypedDict


class User(TypedDict):
    id: str


class UsersResponse(TypedDict):
    data: list[User]
    skip: int
    limit: int
