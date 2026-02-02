import redis.asyncio as redis

from app.config.settings import settings

_client: redis.Redis | None = None


async def init_redis():
    """앱 시작 시 Redis 클라이언트를 초기화한다."""
    global _client
    _client = redis.from_url(settings.redis_url, decode_responses=True)


def get_redis() -> redis.Redis:
    """초기화된 Redis 클라이언트를 반환한다."""
    return _client
