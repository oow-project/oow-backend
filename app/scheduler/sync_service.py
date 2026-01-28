import asyncio
import logging
from datetime import UTC, datetime

import httpx

from app.config.supabase import get_supabase
from app.services.overfast import fetch_hero_detail, fetch_hero_stats, fetch_heroes

logger = logging.getLogger(__name__)

BASE_DELAY = 15
FAILURE_DELAY = 45
MAX_RETRIES = 5

REGIONS = ["asia", "europe", "americas"]
DIVISIONS = [
    "bronze",
    "silver",
    "gold",
    "platinum",
    "diamond",
    "master",
    "grandmaster",
]

async def _fetch_with_retry(fetch_fn, **kwargs) -> list[dict] | dict | None:
    """429/5xx 발생 시 지수 백오프로 재시도한다."""
    for attempt in range(MAX_RETRIES):
        try:
            return await fetch_fn(**kwargs)
        except httpx.HTTPStatusError as e:
            status = e.response.status_code
            is_retryable = status == 429 or status >= 500
            if is_retryable and attempt < MAX_RETRIES - 1:
                retry_after = e.response.headers.get("Retry-After")
                if retry_after:
                    wait = int(retry_after) + 2
                else:
                    wait = 2 ** (attempt + 2)
                logger.warning(
                    "%d 응답 - %d초 대기 후 재시도 (%d/%d)",
                    status, wait, attempt + 1, MAX_RETRIES,
                )
                await asyncio.sleep(wait)
            else:
                raise
    return None


async def _upsert_hero_info(
    supabase,
    hero_list_item: dict,
    detail: dict,
) -> None:
    """영웅 기본 정보를 upsert한다."""
    row = {
        "key": hero_list_item["key"],
        "name": detail.get("name", ""),
        "portrait": hero_list_item.get("portrait", ""),
        "role": detail.get("role", ""),
        "description": detail.get("description", ""),
        "location": detail.get("location"),
        "age": detail.get("age"),
        "hitpoints_health": detail.get("hitpoints", {}).get("health", 0),
        "hitpoints_armor": detail.get("hitpoints", {}).get("armor", 0),
        "hitpoints_shields": detail.get("hitpoints", {}).get("shields", 0),
        "synced_at": datetime.now(UTC).isoformat(),
    }
    await supabase.table("heroes").upsert(row).execute()


async def _upsert_hero_abilities(
    supabase,
    hero_key: str,
    abilities: list[dict],
) -> None:
    """영웅 스킬을 upsert한다."""
    for ability in abilities:
        row = {
            "hero_key": hero_key,
            "name": ability.get("name", ""),
            "description": ability.get("description", ""),
            "icon": ability.get("icon", ""),
        }
        await supabase.table("hero_abilities").upsert(
            row, on_conflict="hero_key,name"
        ).execute()


async def _log_sync(
    supabase,
    task_name: str,
    status: str,
    started_at: datetime,
    error_message: str | None = None,
) -> None:
    """scheduler_logs 테이블에 실행 결과를 기록한다."""
    row = {
        "task_name": task_name,
        "status": status,
        "started_at": started_at.isoformat(),
        "finished_at": datetime.now(UTC).isoformat(),
        "error_message": error_message,
    }
    await supabase.table("scheduler_logs").insert(row).execute()


async def _sync_single_hero(
    supabase, client: httpx.AsyncClient, hero: dict, index: int, total: int
) -> str | None:
    """영웅 1명의 기본 정보 + 스킬을 동기화한다.
    Returns:
        실패 시 hero_key, 성공 시 None
    """
    hero_key = hero["key"]

    try:
        detail = await _fetch_with_retry(
            fetch_hero_detail,
            hero_key=hero_key,
            locale="ko-kr",
            client=client,
        )

        if not detail:
            return hero_key

        await _upsert_hero_info(supabase, hero, detail)
        await _upsert_hero_abilities(
            supabase, hero_key, detail.get("abilities", [])
        )

        logger.info("[%d/%d] %s 동기화 완료", index, total, hero_key)
        return None

    except Exception as e:
        logger.error("[%d/%d] %s 동기화 실패: %s", index, total, hero_key, e)
        return hero_key


def _build_stat_tasks() -> list[dict]:
    """27개 통계 수집 조합을 생성한다."""
    tasks: list[dict] = []

    for region in REGIONS:
        tasks.append({
            "gamemode": "competitive",
            "region": region,
            "division": "all",
            "api_division": None,
        })
        for division in DIVISIONS:
            tasks.append({
                "gamemode": "competitive",
                "region": region,
                "division": division,
                "api_division": division,
            })
        tasks.append({
            "gamemode": "quickplay",
            "region": region,
            "division": "all",
            "api_division": None,
        })

    return tasks


async def _sync_single_stat_task(
    supabase,
    client: httpx.AsyncClient,
    task: dict,
    valid_keys: set[str],
    synced_at: str,
    index: int,
    total: int,
) -> tuple[int, bool]:
    """통계 조합 1건을 동기화한다.
    Returns:
        (저장 수, 성공 여부) 튜플
    """
    gamemode = task["gamemode"]
    region = task["region"]
    division = task["division"]
    api_division = task["api_division"]
    label = f"{region}/{gamemode}/{division}"

    try:
        kwargs: dict = {
            "platform": "pc",
            "gamemode": gamemode,
            "region": region,
            "client": client,
        }
        if api_division:
            kwargs["competitive_division"] = api_division

        stats = await _fetch_with_retry(fetch_hero_stats, **kwargs)

        if stats is None:
            return 0, False

        saved = 0
        for stat in stats:
            if stat["hero"] not in valid_keys:
                continue

            row = {
                "hero_key": stat["hero"],
                "platform": "pc",
                "gamemode": gamemode,
                "region": region,
                "competitive_division": division,
                "winrate": stat.get("winrate"),
                "pickrate": stat.get("pickrate"),
                "synced_at": synced_at,
            }
            await supabase.table("hero_stats").upsert(
                row,
                on_conflict="hero_key,platform,gamemode,region,competitive_division",
            ).execute()
            saved += 1

        logger.info("[%d/%d] %s: %d명 저장", index, total, label, saved)
        return saved, True

    except Exception as e:
        logger.error("[%d/%d] %s 실패: %s", index, total, label, e)
        await asyncio.sleep(FAILURE_DELAY)
        return 0, False

async def sync_heroes() -> None:
    """영웅 기본 정보 + 스킬을 동기화한다. (1일 1회)"""
    started_at = datetime.now(UTC)
    supabase = get_supabase()
    failed_heroes: list[str] = []

    try:
        async with httpx.AsyncClient() as client:
            heroes = await _fetch_with_retry(
                fetch_heroes, locale="ko-kr", client=client
            )

            if not heroes:
                logger.error("영웅 목록을 가져오지 못했습니다")
                await _log_sync(
                    supabase, "sync_heroes", "failed", started_at, "영웅 목록 조회 실패"
                )
                return

            logger.info("총 %d명의 영웅 동기화 시작", len(heroes))

            for i, hero in enumerate(heroes):
                failed_key = await _sync_single_hero(
                    supabase, client, hero, i + 1, len(heroes)
                )
                if failed_key:
                    failed_heroes.append(failed_key)
                await asyncio.sleep(BASE_DELAY)

        status = "failed" if failed_heroes else "success"
        error_msg = (
            f"실패한 영웅: {', '.join(failed_heroes)}" if failed_heroes else None
        )
        await _log_sync(supabase, "sync_heroes", status, started_at, error_msg)

        logger.info(
            "sync_heroes 완료: 성공 %d, 실패 %d",
            len(heroes) - len(failed_heroes),
            len(failed_heroes),
        )

    except Exception as e:
        logger.error("sync_heroes 치명적 오류: %s", e)
        await _log_sync(supabase, "sync_heroes", "failed", started_at, str(e))


async def sync_hero_stats() -> None:
    """영웅 통계를 동기화한다. (1시간 1회)"""
    started_at = datetime.now(UTC)
    supabase = get_supabase()
    synced_at = datetime.now(UTC).isoformat()

    try:
        heroes_result = await supabase.table("heroes").select("key").execute()
        valid_keys: set[str] = {hero["key"] for hero in heroes_result.data}
        logger.info("유효한 영웅 키: %d개", len(valid_keys))

        tasks = _build_stat_tasks()
        total_saved = 0
        failed = 0

        async with httpx.AsyncClient() as client:
            for i, task in enumerate(tasks):
                saved, success = await _sync_single_stat_task(
                    supabase, client, task, valid_keys, synced_at, i + 1, len(tasks)
                )
                total_saved += saved
                if not success:
                    failed += 1
                await asyncio.sleep(BASE_DELAY)

        status = "failed" if failed > 0 else "success"
        error_msg = f"{failed}건 실패" if failed > 0 else None
        await _log_sync(supabase, "sync_hero_stats", status, started_at, error_msg)

        logger.info("sync_hero_stats 완료: %d건 저장, %d건 실패", total_saved, failed)

    except Exception as e:
        logger.error("sync_hero_stats 치명적 오류: %s", e)
        await _log_sync(supabase, "sync_hero_stats", "failed", started_at, str(e))
