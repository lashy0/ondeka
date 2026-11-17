from litestar.config.app import AppConfig
from litestar.di import Provide
from litestar.openapi import OpenAPIConfig
from litestar.openapi.plugins import ScalarRenderPlugin
from litestar.plugins import InitPluginProtocol

from app.settings import get_settings


class ApplicationCore(InitPluginProtocol):
    """Application core configuration plugin."""

    def on_app_init(self, app_config: AppConfig) -> AppConfig:
        """Configure application.

        Args:
            app_config: The application configuration.

        Returns:
            The configured application configuration.
        """
        settings = get_settings()

        app_config.debug = settings.app.debug

        app_config.openapi_config = OpenAPIConfig(
            title=settings.app.name,
            version=settings.app.version,
            render_plugins=[ScalarRenderPlugin()],
        )

        app_config.dependencies.update(
            {
                "settings": Provide(
                    get_settings,
                    sync_to_thread=False,
                ),
            }
        )

        return app_config
