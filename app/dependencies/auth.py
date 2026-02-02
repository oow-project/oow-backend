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
