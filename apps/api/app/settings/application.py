import tomllib
from pathlib import Path

from pydantic import BaseModel


def get_app_version() -> str:
    """Read the application version from project metadata."""
    pyproject = Path(__file__).resolve().parents[2] / "pyproject.toml"

    with pyproject.open("rb") as file:
        data = tomllib.load(file)

        return data["project"]["version"]


class AppSettings(BaseModel):
    """General application settings."""

    name: str = "Ondeka API"
    version: str = get_app_version()

    debug: bool = False
