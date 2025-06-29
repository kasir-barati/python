from fastapi import HTTPException
from pydantic import SecretStr

SPECIAL_CHARS: set[str] = {
    "$",
    "@",
    "#",
    "%",
    "!",
    "^",
    "&",
    "*",
    "(",
    ")",
    "-",
    "_",
    "+",
    "=",
    "{",
    "}",
    "[",
    "]",
}


def validate_password(password: SecretStr) -> SecretStr:
    plain_pass = password.get_secret_value()
    if (
        not any(character.isupper() for character in plain_pass)
        or not any(character.islower() for character in plain_pass)
        or not any(character.isdigit() for character in plain_pass)
        or not any(character in SPECIAL_CHARS for character in plain_pass)
    ):
        raise HTTPException(
            400,
            "Password should have at least one uppercase letter, one lowercase letter, one digit, and one special character.",
        )
    return password
