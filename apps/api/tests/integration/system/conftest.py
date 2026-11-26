import pytest
from sqlalchemy import make_url


@pytest.fixture
def database_name_override() -> str | None:
    return None


@pytest.fixture
def postgres_url(
    postgres_url: str,
    database_name_override: str | None,
) -> str:
    if database_name_override is None:
        return postgres_url

    url = make_url(postgres_url).set(database=database_name_override)

    return url.render_as_string(hide_password=False)
