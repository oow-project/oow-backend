import json
from collections.abc import Callable
from typing import Any

from app.config.redis import get_redis


async def get_or_set_cache(
    key: str,
    fetch_fn: Callable,
    ttl: int,
) -> Any:
    """
    캐시 조회 후 없으면 fetch_fn 실행하여 저장

    Args:
        key: Redis 키
        fetch_fn: 데이터 조회 함수 (async)
        ttl: 캐시 유효 시간 (초)

    Returns:
        캐시된 데이터 또는 새로 조회한 데이터
    """
    redis = get_redis()

    cached = await redis.get(key)
    if cached:
        return json.loads(cached)

    data = await fetch_fn()

    await redis.set(key, json.dumps(data), ex=ttl)

    return data


async def invalidate_cache(cache_key: str) -> int:
    """
    캐시 무효화

    Args:
        cache_key: "cache:heroes:*", "cache:stats:*" 등

    Returns:
        삭제된 키 개수
    """
    redis = get_redis()
    keys = await redis.keys(cache_key)
    if keys:
        return await redis.delete(*keys)
    return 0
