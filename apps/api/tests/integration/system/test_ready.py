import pytest
from httpx import AsyncClient
from litestar.status_codes import HTTP_200_OK, HTTP_503_SERVICE_UNAVAILABLE


async def test_ready(client: AsyncClient):
    response = await client.get("/ready")
    assert response.status_code == HTTP_200_OK

    body = response.json()
    assert body["status"] == "online"


@pytest.mark.parametrize("database_name_override", ["ondeka_missing_database"])
async def test_ready_when_database_is_missing(client: AsyncClient):
    response = await client.get("/ready")
    assert response.status_code == HTTP_503_SERVICE_UNAVAILABLE

    body = response.json()
    assert body["status"] == "offline"
