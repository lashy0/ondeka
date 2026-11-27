from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from .application import AppSettings
from .database import DatabaseSettings
from .logging import LoggingSettings

PROJECT_ROOT = Path(__file__).resolve().parents[4]


class Settings(BaseSettings):
    """Load settings from environment variables and the .env file."""

    model_config = SettingsConfigDict(
        env_prefix="ONDEKA_",
        env_nested_delimiter="__",
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app: AppSettings = Field(default_factory=AppSettings)
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    logging: LoggingSettings = Field(default_factory=LoggingSettings)


@lru_cache
def get_settings() -> Settings:
    """Return the cached application settings."""
    return Settings()
