import pytest
from httpx import AsyncClient
from litestar.status_codes import HTTP_200_OK

from app.settings import get_settings


async def test_health(client: AsyncClient):
    expected = get_settings().app

    response = await client.get("/health")
    assert response.status_code == HTTP_200_OK

    body = response.json()
    assert body["status"] == "ok"
    assert body["app"] == expected.name
    assert body["version"] == expected.version


@pytest.mark.parametrize("database_name_override", ["ondeka_missing_database"])
async def test_health_when_database_is_missing(client: AsyncClient):
    response = await client.get("/health")
    assert response.status_code == HTTP_200_OK

    body = response.json()
    assert body["status"] == "ok"
