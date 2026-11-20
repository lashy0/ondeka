from asyncio import timeout

from advanced_alchemy.exceptions import RepositoryError
from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from asyncpg import InterfaceError, PostgresError
from sqlalchemy.ext.asyncio import AsyncSession

READINESS_TIMEOUT_SECONDS = 2


class ReadinessService:
    """Check the availability of required application dependencies."""

    def __init__(self, db_session: AsyncSession):
        self._db_session = db_session

    async def is_ready(self) -> bool:
        """Check whether database is ready."""
        try:
            async with timeout(READINESS_TIMEOUT_SECONDS):
                return await SQLAlchemyAsyncRepository.check_health(self._db_session)
        except InterfaceError, OSError, PostgresError, RepositoryError:
            return False
