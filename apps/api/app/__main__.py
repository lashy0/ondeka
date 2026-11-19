import os
from pathlib import Path

from litestar.cli.main import litestar_group


def setup_environment() -> None:
    """Configure the environment variables."""
    app_dir = Path(__file__).resolve().parent

    os.environ.setdefault("UVICORN_APP_DIR", str(app_dir))
    os.environ.setdefault("LITESTAR_APP", "app.server.asgi:create_app")


def main() -> None:
    """Application entry point.

    This function sets up the environment and runs the Litestar CLI.
    """
    setup_environment()

    litestar_group(prog_name="python -m app")


if __name__ == "__main__":
    main()
