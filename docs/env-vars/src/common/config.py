from typing import Literal, Optional, TypeAlias
from urllib.parse import quote_plus, urlparse, urlunparse
from pydantic import Field, RedisDsn, ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

Env: TypeAlias = Literal["dev", "prod", "test"]

def read_from_secrets(filename: str) -> str:
    with open(f"/run/secrets/{filename}", "r") as f:
        return f.read().strip()

def attach_credentials_to_url(url: str, username: str, password: str) -> str:
    parsed_url = urlparse(url)
    host = parsed_url.netloc or parsed_url.path

    # Remove existing user info, if any
    if "@" in host:
        host = host.split("@", 1)[-1]

    user_info = f"{quote_plus(username)}:{quote_plus(password)}"
    network_location = f"{user_info}@{host}"
    rebuilt = parsed_url._replace(netloc=network_location)

    return urlunparse(rebuilt)

def read_file(path: str) -> str:
    with open(path, "r") as f:
        return f.read().strip()

class RedisSettings(BaseSettings):
    plain_url: RedisDsn = Field(alias="url")
    username: Optional[str] = Field(alias="username_file")
    password: Optional[str] = Field(alias="password_file")

    @field_validator("username")
    @classmethod
    def load_username(cls, filename: str, validation_info: ValidationInfo):
        if not filename:
            return
        
        return read_from_secrets(filename)

    @field_validator("password")
    @classmethod
    def load_password(cls, filename: str):
        if not filename:
            return
        
        return read_from_secrets(filename)
    
    @property
    def url(self) -> str:
        stringified_url = str(self.plain_url)

        if self.username and self.password:
            return attach_credentials_to_url(
                stringified_url, self.username, self.password
            )

        return stringified_url

class Settings(BaseSettings):
    env: Env = Field(default="dev", alias="env")
    plain_rabbitmq_uri: str = Field(alias="rabbitmq_uri")
    rabbitmq_username: Optional[str] = Field(alias="rabbitmq_username_file")
    rabbitmq_password: Optional[str] = Field(alias="rabbitmq_password_file")
    redis: RedisSettings

    model_config = SettingsConfigDict(env_nested_delimiter='__')

    @field_validator("rabbitmq_username")
    @classmethod
    def load_username(cls, filename: str, validation_info: ValidationInfo):
        if not filename:
            return
        
        return read_from_secrets(filename)

    @field_validator("rabbitmq_password")
    @classmethod
    def load_password(cls, filename: str):
        if not filename:
            return

        return read_from_secrets(filename)

    @property
    def rabbitmq_uri(self):
        if self.rabbitmq_username and self.rabbitmq_password:
            return attach_credentials_to_url(
                self.plain_rabbitmq_uri, self.rabbitmq_username, self.rabbitmq_password
            )

        return self.plain_rabbitmq_uri