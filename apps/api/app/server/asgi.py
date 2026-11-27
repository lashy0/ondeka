from advanced_alchemy.extensions.litestar import SQLAlchemyPlugin
from litestar import Litestar
from litestar.plugins.structlog import StructlogConfig, StructlogPlugin
from litestar_autowire import AutowireConfig, AutowirePlugin
from litestar_granian import GranianPlugin

from app.lib.logging import create_logging_config
from app.server.core import ApplicationCore
from app.settings import get_settings


def create_app() -> Litestar:
    """Create ASGI application.

    Returns:
        The ASGI application.
    """
    settings = get_settings()

    logging_config = create_logging_config(
        settings.logging,
        logger_names=(
            "litestar",
            "_granian",
            "granian.access",
        ),
    )

    return Litestar(
        plugins=[
            ApplicationCore(),
            StructlogPlugin(
                config=StructlogConfig(
                    structlog_logging_config=logging_config,
                    enable_middleware_logging=False,
                ),
            ),
            GranianPlugin(),
            AutowirePlugin(
                config=AutowireConfig(
                    domain_packages="app.domain",
                ),
            ),
            SQLAlchemyPlugin(config=settings.database.get_config()),
        ],
    )
