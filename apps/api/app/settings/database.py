from pathlib import Path

from advanced_alchemy.extensions.litestar import (
    AlembicAsyncConfig,
    EngineConfig,
    SQLAlchemyAsyncConfig,
)
from pydantic import BaseModel, SecretStr

MIGRATION_DIR = Path(__file__).resolve().parents[1] / "db" / "migrations"


class DatabaseSettings(BaseModel):
    """PostgreSQL connection and migration settings."""

    url: SecretStr
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 5
    max_overflow: int = 10
    pool_timeout: int = 30
    pool_pre_ping: bool = True
    migration_ddl_version_table: str = "ddl_version"

    def get_config(self) -> SQLAlchemyAsyncConfig:
        """Build the SQLAlchemy and Alembic configuration."""
        return SQLAlchemyAsyncConfig(
            connection_string=self.url.get_secret_value(),
            engine_config=EngineConfig(
                echo=self.echo,
                echo_pool=self.echo_pool,
                pool_size=self.pool_size,
                max_overflow=self.max_overflow,
                pool_timeout=self.pool_timeout,
                pool_pre_ping=self.pool_pre_ping,
            ),
            alembic_config=AlembicAsyncConfig(
                script_location=str(MIGRATION_DIR),
                script_config=str(MIGRATION_DIR / "alembic.ini"),
                version_table_name=self.migration_ddl_version_table,
                user_module_prefix="aa_types.",
            ),
        )
