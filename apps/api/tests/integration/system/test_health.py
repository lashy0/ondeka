from app.settings import get_settings


async def test_health(client):
    expected = get_settings().app

    response = await client.get("/health")
    assert response.status_code == 200

    body = response.json()
    assert body["status"] == "ok"
    assert body["app"] == expected.name
    assert body["version"] == expected.version
