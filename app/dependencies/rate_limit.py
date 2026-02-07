from fastapi import HTTPException, Request

from app.config.redis import get_redis
from app.dependencies.auth import get_current_user_or_none

GUEST_LIMIT = 3
MEMBER_LIMIT = 15
WINDOW_SECONDS = 6 * 60 * 60


RATE_LIMIT_SCRIPT = """
local current = redis.call('INCR', KEYS[1])

if current == 1 then
    redis.call('EXPIRE', KEYS[1], tonumber(ARGV[2]))
end

local ttl = redis.call('TTL', KEYS[1])

if current > tonumber(ARGV[1]) then
    return {current, ttl, 1}
end

return {current, ttl, 0}
"""


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

    current, ttl, exceeded = await redis.eval(
        RATE_LIMIT_SCRIPT, 1, key, limit, WINDOW_SECONDS
    )

    if exceeded:
        raise HTTPException(
            status_code=429,
            detail={
                "error": "요청 한도를 초과했습니다",
                "limit": limit,
                "reset_after": ttl,
            },
        )

    return {
        "remaining": limit - current,
        "limit": limit,
        "reset": ttl,
    }

