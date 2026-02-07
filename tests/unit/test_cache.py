"""
cache.py 단위 테스트

캐시 분산 락의 3가지 분기를 검증한다:
1. 캐시 Hit → DB 조회 없이 반환
2. 캐시 Miss + 락 획득 → fetch_fn 호출 + 캐시 저장
3. 캐시 Miss + 락 실패 → 대기 후 캐시에서 반환
4. 대기 타임아웃 → 직접 조회 fallback
5. 캐시 무효화 (SCAN 기반)
"""

import json
from unittest.mock import AsyncMock, patch

import pytest

from app.utils.cache import get_or_set_cache, invalidate_cache


@pytest.fixture
def redis(mock_redis):
    return mock_redis


class TestGetOrSetCache:
    """get_or_set_cache 분기 테스트"""

    async def test_캐시_hit이면_db를_조회하지_않는다(self, redis):
        """캐시에 데이터가 있으면 fetch_fn을 호출하지 않아야 한다"""
        cached_data = [{"key": "ana", "name": "Ana"}]
        redis.get.return_value = json.dumps(cached_data)

        fetch_fn = AsyncMock()
        result = await get_or_set_cache("cache:heroes:all", fetch_fn, ttl=3600)

        assert result == cached_data
        fetch_fn.assert_not_called()

    async def test_캐시_miss이고_락_획득하면_db를_조회하고_캐시에_저장한다(self, redis):
        """캐시가 없고 락을 획득하면 fetch_fn 호출 + Redis에 저장해야 한다"""
        redis.get.return_value = None
        redis.set.return_value = True

        fetch_data = [{"key": "ana", "name": "Ana"}]
        fetch_fn = AsyncMock(return_value=fetch_data)

        result = await get_or_set_cache("cache:heroes:all", fetch_fn, ttl=3600)

        assert result == fetch_data
        fetch_fn.assert_called_once()
        redis.delete.assert_called_once_with("lock:cache:heroes:all")

    async def test_캐시_miss이고_락_실패하면_캐시가_채워질_때까지_대기한다(self, redis):
        """락 획득에 실패하면 _wait_for_cache를 통해 대기해야 한다"""
        redis.get.return_value = None
        redis.set.side_effect = [False]

        cached_data = [{"key": "ana", "name": "Ana"}]

        with patch("app.utils.cache._wait_for_cache", new_callable=AsyncMock) as mock_wait:
            mock_wait.return_value = cached_data
            result = await get_or_set_cache("cache:heroes:all", AsyncMock(), ttl=3600)

            assert result == cached_data
            mock_wait.assert_called_once()

    async def test_대기_타임아웃이면_직접_조회한다(self, redis):
        """_wait_for_cache에서 캐시가 계속 비어있으면 직접 fetch_fn을 호출해야 한다"""
        from app.utils.cache import _wait_for_cache

        redis.get.return_value = None

        fallback_data = [{"key": "ana", "name": "Ana"}]
        fetch_fn = AsyncMock(return_value=fallback_data)

        with patch("app.utils.cache.LOCK_WAIT_MAX_RETRIES", 1):
            with patch("app.utils.cache.LOCK_WAIT_INTERVAL", 0):
                result = await _wait_for_cache(redis, "cache:heroes:all", fetch_fn)

        assert result == fallback_data
        fetch_fn.assert_called_once()


class TestInvalidateCache:
    """invalidate_cache 테스트"""

    async def test_패턴과_일치하는_캐시를_삭제한다(self, redis):
        """SCAN으로 패턴 매칭되는 키를 찾아서 삭제해야 한다"""
        redis.scan.return_value = (0, ["cache:heroes:all", "cache:heroes:tank"])
        redis.delete.return_value = 2

        deleted = await invalidate_cache("cache:heroes:*")

        assert deleted == 2
        redis.delete.assert_called_once_with("cache:heroes:all", "cache:heroes:tank")
