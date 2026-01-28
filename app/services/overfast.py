import httpx

OVERFAST_BASE_URL = "https://overfast-api.tekrop.fr"


async def fetch_heroes(
    locale: str | None = None,
    client: httpx.AsyncClient | None = None,
) -> list[dict]:
    """Overfast API에서 영웅 목록을 가져온다.
    Args:
    locale: 예시 ) "ko-kr" / "en-u", None이면 API 기본 값 영어를 사용한다.
    client: 재사용할 httpx 클라이언트. None이면 내부에서 생성
    """
    params: dict[str, str] = {}
    if locale:
        params["locale"] = locale

    if client:
        response = await client.get(
            f"{OVERFAST_BASE_URL}/heroes",
            params=params,
            timeout=30.0,
        )
        response.raise_for_status()
        return response.json()

    async with httpx.AsyncClient() as new_client:
        response = await new_client.get(
            f"{OVERFAST_BASE_URL}/heroes",
            params=params,
            timeout=30.0,
        )
        response.raise_for_status()
        return response.json()


async def fetch_hero_detail(
    hero_key: str,
    locale: str | None = None,
    client: httpx.AsyncClient | None = None,
) -> dict:
    """Overfast API에서 특정 영웅의 상세 정보를 가져온다.
    Args:
    hero_key: 영웅 고유 키 예시 ) "ana" / "doomfist"
    locale: 예시 ) "ko-kr" , "en-us" None이면 API 기본 값 영어를 사용한다.
    client: 재사용할 httpx 클라이언트. None이면 내부에서 생성
    """
    params: dict[str, str] = {}
    if locale:
        params["locale"] = locale

    if client:
        response = await client.get(
            f"{OVERFAST_BASE_URL}/heroes/{hero_key}",
            params=params,
            timeout=30.0,
        )
        response.raise_for_status()
        return response.json()

    async with httpx.AsyncClient() as new_client:
        response = await new_client.get(
            f"{OVERFAST_BASE_URL}/heroes/{hero_key}",
            params=params,
            timeout=30.0,
        )
        response.raise_for_status()
        return response.json()


async def fetch_hero_stats(
    platform: str = "pc",
    gamemode: str = "competitive",
    region: str = "asia",
    competitive_division: str | None = None,
    client: httpx.AsyncClient | None = None,
) -> list[dict]:
    """Overfast API에서 영웅 통계를 가져온다.
    Args:
        platform: "pc" | "console"
        gamemode: "competitive" | "quickplay"
        region: "asia" | "europe" | "americas"
        competitive_division: "bronze" ~ "grandmaster", None이면 전체 통합
        client: 재사용할 httpx 클라이언트. None이면 내부에서 생성
    """
    params: dict[str, str] = {
        "platform": platform,
        "gamemode": gamemode,
        "region": region,
    }
    if competitive_division:
        params["competitive_division"] = competitive_division

    if client:
        response = await client.get(
            f"{OVERFAST_BASE_URL}/heroes/stats",
            params=params,
            timeout=30.0,
        )
        response.raise_for_status()
        return response.json()

    async with httpx.AsyncClient() as new_client:
        response = await new_client.get(
            f"{OVERFAST_BASE_URL}/heroes/stats",
            params=params,
            timeout=30.0,
        )
        response.raise_for_status()
        return response.json()
