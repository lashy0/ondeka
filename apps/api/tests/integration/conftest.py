import pytest
from litestar.testing import AsyncTestClient

from app.server.asgi import create_app


@pytest.fixture
async def client():
    async with AsyncTestClient(app=create_app()) as client:
        yield client
