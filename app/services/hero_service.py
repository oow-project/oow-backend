from app.config.supabase import get_supabase
from app.exceptions import InvalidParameterError, NotFoundError

VALID_ROLES = {"tank", "damage", "support"}
VALID_ROLE_FILTERS = {"all"} | VALID_ROLES
VALID_PLATFORMS = {"pc", "console"}
VALID_GAMEMODES = {"competitive", "quickplay"}
VALID_REGIONS = {"asia", "europe", "americas"}
VALID_DIVISIONS = {
    "all",
    "bronze",
    "silver",
    "gold",
    "platinum",
    "diamond",
    "master",
    "grandmaster",
}
VALID_ORDER_FIELDS = {"winrate", "pickrate"}
VALID_ORDER_DIRS = {"asc", "desc"}


async def get_heroes(role: str = "all") -> list[dict]:
    """영웅 목록을 조회한다."""
    if role not in VALID_ROLE_FILTERS:
        raise InvalidParameterError(
            "유효하지 않은 역할입니다. all, tank, damage, support 중 하나를 입력하세요."
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
    health = hero.get("hitpoints_health", 0)
    armor = hero.get("hitpoints_armor", 0)
    shields = hero.get("hitpoints_shields", 0)

    abilities_response = await supabase.table("hero_abilities").select(
        "name, description, icon, ability_type"
    ).eq("hero_key", hero_key).execute()

    abilities_grouped = {"skill": [], "perk_major": [], "perk_minor": []}
    for ability in abilities_response.data:
        abilities_grouped[ability["ability_type"]].append(ability)

    counter_keys = hero.get("counters") or []
    synergy_keys = hero.get("synergies") or []

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
            "health": health,
            "armor": armor,
            "shields": shields,
            "total": health + armor + shields,
        },
        "abilities": abilities_grouped,
        "counters": [related_map[k] for k in counter_keys if k in related_map],
        "synergies": [related_map[k] for k in synergy_keys if k in related_map],
    }


async def get_hero_stats(
    platform: str = "pc",
    gamemode: str = "competitive",
    region: str = "asia",
    competitive_division: str = "all",
    role: str = "all",
    order_by: str = "winrate:desc",
) -> dict:
    """영웅 통계를 조회한다."""
    if platform not in VALID_PLATFORMS:
        raise InvalidParameterError(
            f"유효하지 않은 플랫폼입니다. {', '.join(VALID_PLATFORMS)} 중 하나를 입력하세요."
        )
    if gamemode not in VALID_GAMEMODES:
        raise InvalidParameterError(
            f"유효하지 않은 게임모드입니다. {', '.join(VALID_GAMEMODES)} 중 하나를 입력하세요."
        )
    if region not in VALID_REGIONS:
        raise InvalidParameterError(
            f"유효하지 않은 지역입니다. {', '.join(VALID_REGIONS)} 중 하나를 입력하세요."
        )
    if competitive_division not in VALID_DIVISIONS:
        raise InvalidParameterError(
            f"유효하지 않은 티어입니다. {', '.join(VALID_DIVISIONS)} 중 하나를 입력하세요."
        )
    if role not in VALID_ROLE_FILTERS:
        raise InvalidParameterError(
            "유효하지 않은 역할입니다. all, tank, damage, support 중 하나를 입력하세요."
        )

    parts = order_by.split(":")
    if len(parts) != 2 or parts[0] not in VALID_ORDER_FIELDS or parts[1] not in VALID_ORDER_DIRS:
        raise InvalidParameterError(
            "유효하지 않은 정렬입니다. 예: winrate:desc, pickrate:asc"
        )
    order_field, order_dir = parts

    supabase = get_supabase()

    query = (
        supabase.table("hero_stats")
        .select("hero_key, winrate, pickrate, synced_at, heroes(name, portrait, role)")
        .eq("platform", platform)
        .eq("gamemode", gamemode)
        .eq("region", region)
        .eq("competitive_division", competitive_division)
    )

    if role != "all":
        query = query.eq("heroes.role", role)

    query = query.order(order_field, desc=(order_dir == "desc"))

    response = await query.execute()

    stats = []
    synced_at = None

    for row in response.data:
        hero = row.get("heroes")
        if not hero:
            continue
        stats.append({
            "key": row["hero_key"],
            "name": hero["name"],
            "portrait": hero["portrait"],
            "role": hero["role"],
            "winrate": row["winrate"],
            "pickrate": row["pickrate"],
        })
        if synced_at is None and row.get("synced_at"):
            synced_at = row["synced_at"]

    return {
        "stats": stats,
        "filters": {
            "platform": platform,
            "gamemode": gamemode,
            "region": region,
            "competitive_division": competitive_division,
            "role": role,
        },
        "total": len(stats),
        "synced_at": synced_at,
    }
