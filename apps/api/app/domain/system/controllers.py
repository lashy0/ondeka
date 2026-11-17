from litestar import Controller, get
from litestar.di import NamedDependency
from litestar.response import Response

from app.settings import Settings

from . import schemas as s


class SystemController(Controller):
    """System health and configuration."""

    tags = ["System"]
    dependencies = {}

    @get(
        operation_id="SystemHealth",
        name="system:health",
        path="/health",
        summary="Health check",
        security=[],
    )
    async def check_system_health(
        self,
        settings: NamedDependency[Settings],
    ) -> Response[s.SystemHealth]:
        """Return application liveness status and metadata.

        Args:
            settings: Application settings.

        Returns:
            The response object.
        """
        return Response(
            content=s.SystemHealth(
                app=settings.app.name,
                version=settings.app.version,
            )
        )
