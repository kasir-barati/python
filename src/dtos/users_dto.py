from typing import Annotated, ClassVar, TypedDict

from pydantic import AfterValidator, BaseModel, ConfigDict, EmailStr, Field, SecretStr

from utils.validate_password_util import validate_password


class User(TypedDict):
    id: str


class CreateUserRequest(BaseModel):
    email: EmailStr
    name: str = Field(min_length=2)
    password: Annotated[SecretStr, AfterValidator(validate_password)]

    model_config: ClassVar[ConfigDict] = ConfigDict(str_strip_whitespace=True)


class UsersResponse(TypedDict):
    data: list[User]
    skip: int
    limit: int
