from collections.abc import AsyncIterator, Iterator

import pytest
from httpx import AsyncClient
from litestar import Litestar
from litestar.testing import AsyncTestClient

from app.server.asgi import create_app
from app.settings import get_settings


@pytest.fixture
async def client(app: Litestar) -> AsyncIterator[AsyncClient]:
    async with AsyncTestClient(app=app) as client:
        yield client


@pytest.fixture
def app(
    postgres_url: str,
    monkeypatch: pytest.MonkeyPatch,
) -> Iterator[Litestar]:
    try:
        with monkeypatch.context() as env:
            env.setenv("ONDEKA_DATABASE__URL", postgres_url)
            get_settings.cache_clear()
            app = create_app()

            yield app
    finally:
        get_settings.cache_clear()
