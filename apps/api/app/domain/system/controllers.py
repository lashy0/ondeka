from litestar import Controller, get
from litestar.di import NamedDependency, Provide
from litestar.openapi.datastructures import ResponseSpec
from litestar.response import Response
from litestar.status_codes import HTTP_200_OK, HTTP_503_SERVICE_UNAVAILABLE

from app.settings import Settings

from . import schemas as s
from .deps import provide_readiness_service
from .services import ReadinessService


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
        status_code=HTTP_200_OK,
        response_description="Application is running",
        description=(
            "Checks whether the API process can respond and returns "
            "the application name and version."
        ),
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

    @get(
        operation_id="SystemReadiness",
        name="system:readiness",
        path="/ready",
        summary="Readiness check",
        security=[],
        status_code=HTTP_200_OK,
        response_description="Application is ready to handle requests",
        description=(
            "Checks whether the application can reach its required dependencies. "
            "Currently checks database connectivity."
        ),
        dependencies={
            "readiness_service": Provide(provide_readiness_service, sync_to_thread=False),
        },
        responses={
            HTTP_503_SERVICE_UNAVAILABLE: ResponseSpec(
                data_container=s.SystemReadiness,
                description="A required dependency is unavailable",
            )
        },
    )
    async def check_system_readiness(
        self,
        readiness_service: NamedDependency[ReadinessService],
    ) -> Response[s.SystemReadiness]:
        """Return application readiness status.

        Args:
            readiness_service: Service to check required application dependencies.

        Returns:
            The response object with HTTP 200 when online, 503 when offline.
        """
        online = await readiness_service.is_ready()

        return Response(
            content=s.SystemReadiness(status="online" if online else "offline"),
            status_code=HTTP_200_OK if online else HTTP_503_SERVICE_UNAVAILABLE,
        )
