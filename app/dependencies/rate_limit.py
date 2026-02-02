from fastapi import HTTPException, Request

from app.config.redis import get_redis
from app.dependencies.auth import get_current_user_or_none

GUEST_LIMIT = 3
MEMBER_LIMIT = 15
WINDOW_SECONDS = 6 * 60 * 60


async def check_rate_limit(request: Request) -> dict:
    """
    Rate Limit을 체크하는 의존성

    - 비회원: IP 기반, 6시간당 3회
    - 회원: user_id 기반, 6시간당 15회

    Returns:
        dict: {"remaining": 남은 횟수}

    Raises:
        HTTPException: 429 - 요청 한도 초과 시
    """
    redis = get_redis()

    user = await get_current_user_or_none(request)
    user_id = user["id"] if user else None

    if user_id:
        key = f"rate:user:{user_id}"
        limit = MEMBER_LIMIT
    else:
        ip = request.client.host
        key = f"rate:guest:{ip}"
        limit = GUEST_LIMIT

    current = await redis.get(key)
    current = int(current) if current else 0

    ttl = await redis.ttl(key)
    if ttl < 0:
        ttl = WINDOW_SECONDS

    if current >= limit:
        raise HTTPException(
            status_code=429,
            detail={
                "error": "요청 한도를 초과했습니다",
                "limit": limit,
                "reset_after": ttl,
            },
        )

    pipe = redis.pipeline()
    pipe.incr(key)
    pipe.expire(key, WINDOW_SECONDS)
    await pipe.execute()

    return {
        "remaining": limit - current - 1,
        "limit": limit,
        "reset": WINDOW_SECONDS,
    }
