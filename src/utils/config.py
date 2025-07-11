from typing import ClassVar

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = r"/\/\y @P!"
    rabbitmq_uri: str

    # This is how you can shorten the env variable name
    # some_var: str = Field(alias="some_env_var")

    # model_config is used for Pydantic configuration
    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_file=".env", extra="ignore"
    )
