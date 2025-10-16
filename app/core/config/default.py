from os import environ

from pydantic_settings import BaseSettings, SettingsConfigDict


class DefaultSettings(BaseSettings):
    """
    Default configs for application.
    """

    ENV: str = environ.get("ENV", "local")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # важно: теперь не будет ошибок про лишние переменные
    )

    @property
    def database_uri(self) -> str:
        return "sqlite+aiosqlite:///./my_database.db"

    @property
    def database_uri_sync(self) -> str:
        return "sqlite:///./my_database.db"
