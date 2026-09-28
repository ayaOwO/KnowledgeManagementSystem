from dataclasses import field

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    openai_api_key: str = field(default="")
    openai_endpoint: str = field()
    openai_model: str = field()
    database_url: str = field()
    model_config = SettingsConfigDict(env_file=".env")
