import asyncio
import json
import logging
from collections.abc import Callable
from typing import Any

from app.config.redis import get_redis

logger = logging.getLogger(__name__)

LOCK_TIMEOUT = 10
LOCK_WAIT_INTERVAL = 0.1
LOCK_WAIT_MAX_RETRIES = 50


async def _wait_for_cache(redis, key: str, fetch_fn: Callable) -> Any:
    """락을 획득하지 못한 요청이 캐시가 채워질 때까지 대기한다."""
    for _ in range(LOCK_WAIT_MAX_RETRIES):
        await asyncio.sleep(LOCK_WAIT_INTERVAL)
        cached = await redis.get(key)

        if cached:
            return json.loads(cached)

    logger.warning("캐시 대기 타임아웃, 직접 조회: %s", key)
    return await fetch_fn()


async def get_or_set_cache(
    key: str,
    fetch_fn: Callable,
    ttl: int,
) -> Any:
    """
    캐시를 조회하고, 없으면 분산 락을 사용하여 단일 요청만 DB를 조회한다.

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

    lock_key = f"lock:{key}"
    acquired = await redis.set(lock_key, "1", nx=True, ex=LOCK_TIMEOUT)

    if not acquired:
        return await _wait_for_cache(redis, key, fetch_fn)

    try:
        data = await fetch_fn()
        await redis.set(key, json.dumps(data), ex=ttl)

        return data
    finally:
        await redis.delete(lock_key)


async def invalidate_cache(pattern: str, batch_size: int = 100) -> int:
    """
    패턴과 일치하는 캐시를 삭제한다.

    Args:
        pattern: 삭제할 캐시 키 패턴 (예: "cache:heroes:*")
        batch_size: SCAN 1회당 스캔할 키 수

    Returns:
        삭제된 키 개수
    """
    redis = get_redis()
    cursor = 0
    deleted = 0

    while True:
        cursor, keys = await redis.scan(cursor, match=pattern, count=batch_size)

        if keys:
            deleted += await redis.delete(*keys)

        if cursor == 0:
            break

    return deleted
