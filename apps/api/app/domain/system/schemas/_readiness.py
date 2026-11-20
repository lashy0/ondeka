from typing import Literal

from app.lib.schema import CamelizeBaseStruct

OnlineOffline = Literal["online", "offline"]


class SystemReadiness(CamelizeBaseStruct):
    """Application readiness status."""

    status: OnlineOffline
