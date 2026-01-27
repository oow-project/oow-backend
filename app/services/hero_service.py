from app.config.supabase import get_supabase
from app.exceptions import InvalidParameterError, NotFoundError

VALID_ROLES = {"all", "tank", "damage", "support"}


async def get_heroes(role: str = "all") -> list[dict]:
    """영웅 목록을 조회한다."""
    if role not in VALID_ROLES:
        raise InvalidParameterError(
            "유효하지 않은 역할입니다. tank, damage, support 중 하나를 입력하세요."
        )

    supabase = get_supabase()
    query = supabase.table("heroes").select("key, name, portrait, role")

    if role != "all":
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

    counters_response = await supabase.table("hero_counters").select(
        "counter_key"
    ).eq("hero_key", hero_key).execute()
    counter_keys = [c["counter_key"] for c in counters_response.data]

    synergies_response = await supabase.table("hero_synergies").select(
        "synergy_key"
    ).eq("hero_key", hero_key).execute()
    synergy_keys = [s["synergy_key"] for s in synergies_response.data]

    related_keys = list(set(counter_keys + synergy_keys))
    if related_keys:
        related_response = await supabase.table("heroes").select(
            "key, name, portrait, role"
        ).in_("key", related_keys).execute()
        related_map = {h["key"]: h for h in related_response.data}
    else:
        related_map = {}

    return {
        "key": hero["key"],
        "name": hero["name"],
        "portrait": hero["portrait"],
        "role": hero["role"],
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
        "counters": [related_map[k] for k in counter_keys if k in related_map],
        "synergies": [related_map[k] for k in synergy_keys if k in related_map],
    }
