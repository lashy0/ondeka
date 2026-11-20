from advanced_alchemy.extensions.litestar import SQLAlchemyPlugin
from litestar import Litestar
from litestar_autowire import AutowireConfig, AutowirePlugin

from app.server.core import ApplicationCore
from app.settings import get_settings


def create_app() -> Litestar:
    """Create ASGI application.

    Returns:
        The ASGI application.
    """
    return Litestar(
        plugins=[
            ApplicationCore(),
            AutowirePlugin(
                AutowireConfig(domain_packages="app.domain"),
            ),
            SQLAlchemyPlugin(get_settings().database.get_config()),
        ],
    )
