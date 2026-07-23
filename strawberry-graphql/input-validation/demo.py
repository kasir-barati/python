from __future__ import annotations

import uuid
from typing import Annotated

import strawberry
from pydantic import EmailStr, StringConstraints
from strawberry.asgi import GraphQL

from pydantic_validation import apply_pydantic_validation


@strawberry.input
class UserInfoInput:
    name: Annotated[
        str,
        StringConstraints(strip_whitespace=True, min_length=1, max_length=100),
    ]
    """Name of the user."""
    email: Annotated[str, EmailStr]
    """Email address of the user."""
    password: Annotated[
        str,
        StringConstraints(min_length=8, max_length=128),
    ]
    """Password for the user account."""


@strawberry.type
class UserOutput:
    id: str
    """Unique identifier for the user."""
    name: str
    """Name of the user."""
    email: str
    """Email address of the user."""


@strawberry.type
class Query:
    ping: str = strawberry.field(default="pong")


@strawberry.type
class Mutation:
    @strawberry.mutation
    def echo(
        self,
        text: Annotated[
            str,
            StringConstraints(strip_whitespace=True, min_length=1, max_length=5),
        ],
    ) -> str:
        return text

    @strawberry.mutation
    def create_user(self, user: UserInfoInput) -> UserOutput:
        return UserOutput(
            id=str(uuid.uuid4()),
            name=user.name,
            email=user.email,
        )


apply_pydantic_validation(Query, Mutation)

schema = strawberry.Schema(query=Query, mutation=Mutation)
app = GraphQL(schema)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
