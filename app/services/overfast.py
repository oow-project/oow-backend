import httpx

OVERFAST_BASE_URL = "https://overfast-api.tekrop.fr"

async def fetch_heroes() -> list[dict]:
    """Overfast API에서 영웅 목록을 가져온다."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{OVERFAST_BASE_URL}/heroes", timeout=30.0)
        response.raise_for_status()
        return response.json()



async def fetch_hero_detail(hero_key: str) -> dict:
    """Overfast API에서 특정 영웅의 상세 정보를 가져온다."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{OVERFAST_BASE_URL}/heroes/{hero_key}", timeout=30.0
        )
        response.raise_for_status()
        return response.json()
