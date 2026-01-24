from app.config.supabase import get_supabase
from app.exceptions import InvalidParameterError

VALID_ROLES = {"tank", "damage", "support"}


async def get_heroes(role: str | None = None) -> list[dict]:
    """영웅 목록을 조회한다."""
    if role is not None and role not in VALID_ROLES:
        raise InvalidParameterError(
            "유효하지 않은 역할입니다. tank, damage, support 중 하나를 입력하세요."
        )

    supabase = get_supabase()
    query = supabase.table("heroes").select("key, name, portrait, role")

    if role:
        query = query.eq("role", role)

    response = await query.execute()
    return response.data
