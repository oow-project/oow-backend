from app.config.supabase import get_supabase
from app.exceptions import InvalidParameterError, NotFoundError

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


async def get_hero_detail(hero_key: str) -> dict:
    """영웅 상세 정보를 조회한다."""
    supabase = get_supabase()

    hero_response = await supabase.table("heroes").select("*").eq("key", hero_key).execute()

    if not hero_response.data:
        raise NotFoundError("존재하지 않는 영웅입니다")

    hero = hero_response.data[0]

    abilities_response = await supabase.table("hero_abilities").select(
        "name, description, icon"
    ).eq("hero_key", hero_key).execute()

    perks_response = await supabase.table("hero_perks").select(
        "name, description, icon, type"
    ).eq("hero_key", hero_key).execute()

    return {
        "key": hero["key"],
        "name": hero["name"],
        "portrait": hero["portrait"],
        "role": hero["role"],
        "description": hero.get("description"),
        "location": hero.get("location"),
        "age": hero.get("age"),
        "hitpoints": {
            "health": hero.get("hitpoints_health", 0),
            "armor": hero.get("hitpoints_armor", 0),
            "shields": hero.get("hitpoints_shields", 0),
            "total": (
                hero.get("hitpoints_health", 0)
                + hero.get("hitpoints_armor", 0)
                + hero.get("hitpoints_shields", 0)
            ),
        },
        "abilities": abilities_response.data,
        "perks": perks_response.data,
    }
