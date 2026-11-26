from collections.abc import Iterator

import pytest
from pytest_databases.types import ServiceContainer
from sqlalchemy import URL

POSTGRES_ENV = {
    "POSTGRES_USER": "ondeka",
    "POSTGRES_PASSWORD": "ondeka_test",
    "POSTGRES_DB": "ondeka_test",
}


def _postgres_is_ready(service: ServiceContainer) -> bool:
    result = service.container.exec_run(
        [
            "pg_isready",
            "-h",
            "localhost",
            "-U",
            POSTGRES_ENV["POSTGRES_USER"],
            "-d",
            POSTGRES_ENV["POSTGRES_DB"],
        ]
    )

    return result.exit_code == 0


@pytest.fixture(scope="session")
def postgres_url(docker_service) -> Iterator[str]:
    with docker_service.run(
        image="postgres:18-alpine",
        container_port=5432,
        name="ondeka-test-postgres",
        env=POSTGRES_ENV,
        check=_postgres_is_ready,
        timeout=30,
        transient=True,
    ) as postgres:
        url = URL.create(
            "postgresql+asyncpg",
            username=POSTGRES_ENV["POSTGRES_USER"],
            password=POSTGRES_ENV["POSTGRES_PASSWORD"],
            host=postgres.host,
            port=postgres.port,
            database=POSTGRES_ENV["POSTGRES_DB"],
        )

        yield url.render_as_string(hide_password=False)
