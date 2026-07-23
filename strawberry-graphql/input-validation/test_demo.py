from __future__ import annotations

import re
import uuid

import pytest

from demo import schema


@pytest.mark.asyncio
async def test_echo_valid_short_input_is_accepted() -> None:
    result = await schema.execute(
        "mutation ($t: String!) { echo(text: $t) }",
        variable_values={"t": "hi"},
    )

    assert result.errors is None
    assert result.data == {"echo": "hi"}


@pytest.mark.asyncio
async def test_echo_whitespace_is_stripped() -> None:
    result = await schema.execute(
        "mutation ($t: String!) { echo(text: $t) }",
        variable_values={"t": "  hi  "},
    )

    assert result.errors is None
    assert result.data == {"echo": "hi"}


@pytest.mark.asyncio
async def test_echo_input_longer_than_max_length_is_rejected() -> None:
    result = await schema.execute(
        "mutation ($t: String!) { echo(text: $t) }",
        variable_values={"t": "way too long"},
    )

    assert result.errors is not None
    assert "text" in str(result.errors[0].message)


@pytest.mark.asyncio
async def test_echo_whitespace_only_input_is_rejected() -> None:
    result = await schema.execute(
        "mutation ($t: String!) { echo(text: $t) }",
        variable_values={"t": "   "},
    )

    assert result.errors is not None


@pytest.mark.asyncio
async def test_echo_empty_input_is_rejected() -> None:
    result = await schema.execute(
        "mutation ($t: String!) { echo(text: $t) }",
        variable_values={"t": ""},
    )

    assert result.errors is not None


CREATE_USER = """
mutation ($user: UserInfoInput!) {
  createUser(user: $user) {
    id
    name
    email
  }
}
"""


def _uuid_looks_valid(value: str) -> bool:
    try:
        uuid.UUID(value)
        return True
    except ValueError:
        return False


@pytest.mark.asyncio
async def test_create_user_valid_input_returns_user_with_uuid() -> None:
    result = await schema.execute(
        CREATE_USER,
        variable_values={
            "user": {
                "name": "Ada Lovelace",
                "email": "ada@example.com",
                "password": "s3cret-password",
            }
        },
    )

    assert result.errors is None
    data = result.data["createUser"]
    assert _uuid_looks_valid(data["id"])
    assert data["name"] == "Ada Lovelace"
    assert data["email"] == "ada@example.com"
    # password must not leak into the response schema at all
    assert "password" not in data


@pytest.mark.asyncio
async def test_create_user_trims_whitespace_in_name() -> None:
    result = await schema.execute(
        CREATE_USER,
        variable_values={
            "user": {
                "name": "   Ada Lovelace   ",
                "email": "ada@example.com",
                "password": "s3cret-password",
            }
        },
    )

    assert result.errors is None
    assert result.data["createUser"]["name"] == "Ada Lovelace"


@pytest.mark.asyncio
async def test_create_user_invalid_email_is_rejected() -> None:
    result = await schema.execute(
        CREATE_USER,
        variable_values={
            "user": {
                "name": "Ada",
                "email": "not-an-email",
                "password": "s3cret-password",
            }
        },
    )

    assert result.errors is not None
    assert re.search(r"email", str(result.errors[0].message), re.IGNORECASE)


@pytest.mark.asyncio
async def test_create_user_short_password_is_rejected() -> None:
    result = await schema.execute(
        CREATE_USER,
        variable_values={
            "user": {
                "name": "Ada",
                "email": "ada@example.com",
                "password": "short",
            }
        },
    )

    assert result.errors is not None
    assert re.search(r"password", str(result.errors[0].message), re.IGNORECASE)


@pytest.mark.asyncio
async def test_create_user_empty_name_is_rejected() -> None:
    result = await schema.execute(
        CREATE_USER,
        variable_values={
            "user": {
                "name": "   ",
                "email": "ada@example.com",
                "password": "s3cret-password",
            }
        },
    )

    assert result.errors is not None
    assert re.search(r"name", str(result.errors[0].message), re.IGNORECASE)
