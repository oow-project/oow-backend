from supabase import AsyncClient, acreate_client

from app.config.settings import settings

_client: AsyncClient | None = None


async def init_supabase():
    """앱 시작 시 Supabase 클라이언트를 초기화한다."""
    global _client
    _client = await acreate_client(settings.supabase_url, settings.supabase_key)


def get_supabase() -> AsyncClient:
    """초기화된 Supabase 클라이언트를 반환한다."""
    if _client is None:
        raise RuntimeError("Supabase가 초기화되지 않았습니다. init_supabase()를 먼저 호출하세요.")
    return _client
