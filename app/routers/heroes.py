from fastapi import APIRouter, Path, Query

from app.schemas.hero import HeroDetailResponse, HeroListResponse, StatsResponse
from app.services.hero_service import get_hero_detail, get_hero_stats
from app.services.hero_service import get_heroes as get_heroes_service
from app.utils.cache import get_or_set_cache

router = APIRouter(prefix="/api/heroes", tags=["heroes"])

HEROES_CACHE_TTL = 3600
STATS_CACHE_TTL = 1800
HERO_DETAIL_CACHE_TTL = 3600


@router.get("", response_model=HeroListResponse)
async def get_heroes(role: str = Query(default="all")):
    """영웅 목록을 조회한다."""
    cache_key = f"cache:heroes:{role}"

    heroes = await get_or_set_cache(
        key=cache_key,
        fetch_fn=lambda: get_heroes_service(role),
        ttl=HEROES_CACHE_TTL,
    )

    return HeroListResponse(heroes=heroes, total=len(heroes))


@router.get("/stats", response_model=StatsResponse)
async def get_stats(
    platform: str = Query(default="pc"),
    gamemode: str = Query(default="competitive"),
    region: str = Query(default="asia"),
    competitive_division: str = Query(default="all"),
    role: str = Query(default="all"),
    order_by: str = Query(default="winrate:desc"),
):
    """영웅 통계를 조회한다."""
    cache_key = f"cache:stats:{platform}:{gamemode}:{region}:{competitive_division}:{role}:{order_by}"

    return await get_or_set_cache(
        key=cache_key,
        fetch_fn=lambda: get_hero_stats(
            platform=platform,
            gamemode=gamemode,
            region=region,
            competitive_division=competitive_division,
            role=role,
            order_by=order_by,
        ),
        ttl=STATS_CACHE_TTL,
    )


@router.get("/{hero_key}", response_model=HeroDetailResponse)
async def get_hero(hero_key: str = Path(description="영웅 고유 키 (예: ana, dva)")):
    """영웅 상세 정보를 조회한다."""
    cache_key = f"cache:heroDetail:{hero_key}"

    return await get_or_set_cache(
        key=cache_key,
        fetch_fn=lambda: get_hero_detail(hero_key),
        ttl=HERO_DETAIL_CACHE_TTL,
    )
