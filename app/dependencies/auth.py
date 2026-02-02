from fastapi import HTTPException, Request, status

from app.config.supabase import get_supabase


async def get_current_user(request: Request) -> dict:
    """
    현재 로그인한 사용자를 반환하는 의존성

    - Authorization 헤더에서 Bearer 토큰 추출
    - Supabase로 토큰 검증
    - 검증 실패 시 401 에러

    Returns:
        dict: {"id": user_id, "email": email}

    Raises:
        HTTPException: 401 - 인증 실패 시
    """
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="인증이 필요합니다",
        )

    if not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="잘못된 인증 형식입니다",
        )

    token = auth_header.replace("Bearer ", "")

    supabase = get_supabase()

    try:
        user_response = await supabase.auth.get_user(token)
        user = user_response.user

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="유효하지 않은 토큰입니다",
            )

        return {
            "id": user.id,
            "email": user.email,
        }
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="토큰 검증에 실패했습니다",
        ) from None


async def get_current_user_or_none(request: Request) -> dict | None:
    """
    현재 사용자를 반환하거나, 인증 실패 시 None 반환 (에러 없음)

    - Rate Limit에서 회원/비회원 구분에 사용
    - 토큰이 없거나 유효하지 않으면 None 반환
    """
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return None

    if not auth_header.startswith("Bearer "):
        return None

    token = auth_header.removeprefix("Bearer ")
    supabase = get_supabase()

    try:
        user_response = await supabase.auth.get_user(token)
        user = user_response.user

        if not user:
            return None

        return {"id": user.id, "email": user.email}
    except Exception:
        return None
