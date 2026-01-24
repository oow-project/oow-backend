from fastapi import APIRouter, Query

from app.models.hero import HeroListResponse
from app.services.hero_service import get_heroes as get_heroes_service

router = APIRouter(prefix="/api/heroes", tags=["heroes"])


@router.get("", response_model=HeroListResponse)
async def get_heroes(role: str | None = Query(default=None)):
    """영웅 목록을 조회한다."""
    heroes = await get_heroes_service(role)
    return HeroListResponse(heroes=heroes, total=len(heroes))
