import sys

from litestar.cli.main import litestar_group


def main() -> None:
    """Run Litestar commands."""
    litestar_group(
        args=[
            "--app",
            "app.server.asgi:create_app",
            *sys.argv[1:],
        ],
        prog_name="python -m app",
    )


if __name__ == "__main__":
    main()
