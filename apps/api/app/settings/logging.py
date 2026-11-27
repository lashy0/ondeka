from typing import Literal

from pydantic import BaseModel


class LoggingSettings(BaseModel):
    """Logging level and output format."""

    level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    format: Literal["console", "json"] = "console"
