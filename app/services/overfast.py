import httpx

OVERFAST_BASE_URL = "https://overfast-api.tekrop.fr"


async def fetch_heroes(locale: str | None = None) -> list[dict]:
    """Overfast API에서 영웅 목록을 가져온다.
    Args:
     locale: 예시 ) "ko-kr" / "en-u", None이면 API 기본 값 영어를 사용한다.
    """
    params: dict[str, str] = {}
    if locale:
        params["locale"] = locale

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{OVERFAST_BASE_URL}/heroes",
            params=params,
            timeout=30.0,
        )
        response.raise_for_status()
        return response.json()


async def fetch_hero_detail(hero_key: str, locale: str | None = None) -> dict:
    """Overfast API에서 특정 영웅의 상세 정보를 가져온다.
    Args:
     hero_key: 영웅 고유 키 예시 ) "ana" / "doomfist"
        locale: 예시 ) "ko-kr" , "en-us" None이면 API 기본 값 영어를 사용한다.
    """
    params: dict[str, str] = {}
    if locale:
        params["locale"] = locale

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{OVERFAST_BASE_URL}/heroes/{hero_key}",
            params=params,
            timeout=30.0,
        )
        response.raise_for_status()
        return response.json()
