from litestar.di import NamedDependency
from sqlalchemy.ext.asyncio import AsyncSession

from .services import ReadinessService


def provide_readiness_service(
    db_session: NamedDependency[AsyncSession],
) -> ReadinessService:
    """Provide the application readiness service."""
    return ReadinessService(db_session)
