from supabase import AsyncClient, acreate_client

from app.config.settings import settings

_client: AsyncClient | None = None


async def init_supabase():
    """앱 시작 시 Supabase 클라이언트를 초기화한다."""
    global _client
    _client = await acreate_client(settings.supabase_url, settings.supabase_key)


def get_supabase() -> AsyncClient:
    """초기화된 Supabase 클라이언트를 반환한다."""
    return _client
