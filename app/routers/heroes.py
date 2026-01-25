from fastapi import APIRouter, Path, Query

from app.models.hero import HeroDetailResponse, HeroListResponse
from app.services.hero_service import get_hero_detail
from app.services.hero_service import get_heroes as get_heroes_service

router = APIRouter(prefix="/api/heroes", tags=["heroes"])


@router.get("", response_model=HeroListResponse)
async def get_heroes(role: str | None = Query(default=None)):
    """영웅 목록을 조회한다."""
    heroes = await get_heroes_service(role)
    return HeroListResponse(heroes=heroes, total=len(heroes))


@router.get("/{hero_key}", response_model=HeroDetailResponse)
async def get_hero(hero_key: str = Path(description="영웅 고유 키 (예: ana, dva)")):
    """영웅 상세 정보를 조회한다."""
    return await get_hero_detail(hero_key)
