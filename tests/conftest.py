"""
공통 Fixture 정의

- mock_supabase: Supabase 클라이언트를 모킹하여 실제 DB 없이 테스트
- mock_redis: Redis 클라이언트를 모킹하여 실제 Redis 없이 테스트
- client: FastAPI TestClient (통합 테스트용)
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from httpx import ASGITransport, AsyncClient


@pytest.fixture
def mock_supabase():
    """Supabase 클라이언트 모킹"""
    mock = MagicMock()
    mock.table.return_value = mock
    mock.select.return_value = mock
    mock.insert.return_value = mock
    mock.delete.return_value = mock
    mock.eq.return_value = mock
    mock.in_.return_value = mock
    mock.order.return_value = mock
    mock.limit.return_value = mock
    mock.execute = AsyncMock()
    mock.auth.get_user = AsyncMock()

    with patch("app.config.supabase.get_supabase", return_value=mock):
        yield mock


@pytest.fixture
def mock_redis():
    """Redis 클라이언트 모킹"""
    mock = AsyncMock()
    mock.get = AsyncMock(return_value=None)
    mock.set = AsyncMock(return_value=True)
    mock.delete = AsyncMock()
    mock.eval = AsyncMock()
    mock.scan = AsyncMock(return_value=(0, []))

    with patch("app.config.redis.get_redis", return_value=mock):
        yield mock


@pytest.fixture
async def client(mock_supabase, mock_redis):
    """FastAPI 통합 테스트용 AsyncClient"""
    with (
        patch("app.main.init_supabase"),
        patch("app.main.init_redis"),
        patch("app.main.init_llm"),
        patch("app.main.start_scheduler"),
        patch("app.main.shutdown_scheduler"),
    ):
        from app.main import app

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            yield ac
