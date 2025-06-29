from typing import Annotated, TypedDict

from pydantic import AfterValidator, BaseModel, EmailStr, SecretStr

from utils.validate_password_util import validate_password


class User(TypedDict):
    id: str


class CreateUserRequest(BaseModel):
    email: EmailStr
    password: Annotated[SecretStr, AfterValidator(validate_password)]


class UsersResponse(TypedDict):
    data: list[User]
    skip: int
    limit: int
