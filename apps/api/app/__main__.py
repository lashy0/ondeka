import os

from litestar.cli.main import litestar_group


def setup_environment() -> None:
    """Configure the environment variables."""
    os.environ.setdefault("LITESTAR_APP", "app.server.asgi:create_app")


def main() -> None:
    """Application entry point.

    This function sets up the environment and runs the Litestar CLI.
    """
    setup_environment()

    litestar_group(
        prog_name="python -m app",
        default_map={"run": {"log_access_enabled": True}},
    )


if __name__ == "__main__":
    main()
