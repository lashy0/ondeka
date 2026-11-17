from typing import Literal

from app.lib.schema import CamelizeBaseStruct


class SystemHealth(CamelizeBaseStruct):
    """Application liveness status and metadata."""

    app: str
    version: str
    status: Literal["ok"] = "ok"
