from fastapi import APIRouter, Path, Query

from app.models.hero import HeroDetailResponse, HeroListResponse, StatsResponse
from app.services.hero_service import get_hero_detail, get_hero_stats
from app.services.hero_service import get_heroes as get_heroes_service

router = APIRouter(prefix="/api/heroes", tags=["heroes"])


@router.get("", response_model=HeroListResponse)
async def get_heroes(role: str = Query(default="all")):
    """영웅 목록을 조회한다."""
    heroes = await get_heroes_service(role)
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
    return await get_hero_stats(
        platform=platform,
        gamemode=gamemode,
        region=region,
        competitive_division=competitive_division,
        role=role,
        order_by=order_by,
    )


@router.get("/{hero_key}", response_model=HeroDetailResponse)
async def get_hero(hero_key: str = Path(description="영웅 고유 키 (예: ana, dva)")):
    """영웅 상세 정보를 조회한다."""
    return await get_hero_detail(hero_key)
