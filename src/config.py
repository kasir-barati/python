from typing import ClassVar
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = r"/\/\y @P!"

    # model_config is used for Pydantic configuration
    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(env_file='.env')
