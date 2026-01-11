import pytest
from httpx import AsyncClient
from httpx import ASGITransport
from asgi_lifespan import LifespanManager
from app.main import app


@pytest.fixture
async def client():
    # Оборачиваем app в LifespanManager
    async with LifespanManager(app):
        # Используем ASGITransport для передачи app
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            yield client
