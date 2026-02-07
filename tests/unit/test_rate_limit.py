"""
rate_limit.py 단위 테스트

Lua 스크립트 기반 Rate Limit의 핵심 동작을 검증한다:
1. 비회원 요청 → IP 기반 키, GUEST_LIMIT 적용
2. 회원 요청 → user_id 기반 키, MEMBER_LIMIT 적용
3. 한도 초과 → 429 HTTPException 발생
4. 정상 요청 → remaining, limit, reset 반환
"""

from unittest.mock import AsyncMock, patch

import pytest
from fastapi import HTTPException

from app.dependencies.rate_limit import (
    GUEST_LIMIT,
    MEMBER_LIMIT,
    check_rate_limit,
)


def _make_request(ip="127.0.0.1", auth_header=None):
    """테스트용 가짜 Request 생성"""
    request = AsyncMock()
    request.client.host = ip
    request.headers = {}

    if auth_header:
        request.headers["Authorization"] = auth_header

    return request


class TestCheckRateLimit:
    """check_rate_limit 의존성 테스트"""

    async def test_비회원_첫_요청이면_guest_키와_limit이_적용된다(self, mock_redis):
        """Authorization 없으면 IP 기반 rate:guest 키를 사용해야 한다"""
        mock_redis.eval.return_value = (1, 21600, 0)

        request = _make_request(ip="192.168.1.1")

        with patch("app.dependencies.rate_limit.get_current_user_or_none", return_value=None):
            result = await check_rate_limit(request)

        assert result["remaining"] == GUEST_LIMIT - 1
        assert result["limit"] == GUEST_LIMIT
        assert result["reset"] == 21600

        call_args = mock_redis.eval.call_args
        assert "rate:guest:192.168.1.1" in call_args[0]

    async def test_회원_요청이면_user_키와_member_limit이_적용된다(self, mock_redis):
        """인증된 사용자는 user_id 기반 rate:user 키를 사용해야 한다"""
        mock_redis.eval.return_value = (1, 21600, 0)

        request = _make_request(auth_header="Bearer valid-token")
        mock_user = {"id": "user-123", "email": "test@test.com"}

        with patch("app.dependencies.rate_limit.get_current_user_or_none", return_value=mock_user):
            result = await check_rate_limit(request)

        assert result["remaining"] == MEMBER_LIMIT - 1
        assert result["limit"] == MEMBER_LIMIT

        call_args = mock_redis.eval.call_args
        assert "rate:user:user-123" in call_args[0]

    async def test_한도_초과시_429_에러가_발생한다(self, mock_redis):
        """Lua 스크립트가 exceeded=1을 반환하면 429 HTTPException이 발생해야 한다"""
        mock_redis.eval.return_value = (4, 18000, 1)

        request = _make_request()

        with patch("app.dependencies.rate_limit.get_current_user_or_none", return_value=None):
            with pytest.raises(HTTPException) as exc_info:
                await check_rate_limit(request)

        assert exc_info.value.status_code == 429
        assert exc_info.value.detail["reset_after"] == 18000

    async def test_정상_요청_응답에_remaining과_limit과_reset이_포함된다(self, mock_redis):
        """정상 요청 시 남은 횟수, 총 한도, 리셋 시간이 모두 반환되어야 한다"""
        mock_redis.eval.return_value = (2, 15000, 0)

        request = _make_request()

        with patch("app.dependencies.rate_limit.get_current_user_or_none", return_value=None):
            result = await check_rate_limit(request)

        assert "remaining" in result
        assert "limit" in result
        assert "reset" in result
        assert result["remaining"] == GUEST_LIMIT - 2
