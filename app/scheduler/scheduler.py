import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.scheduler.sync_service import sync_hero_stats, sync_heroes

logger = logging.getLogger(__name__)

_scheduler: AsyncIOScheduler | None = None


def start_scheduler() -> None:
    """스케줄러 시작"""
    scheduler_logger = logging.getLogger("app.scheduler")
    scheduler_logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    )
    scheduler_logger.addHandler(handler)

    global _scheduler
    _scheduler = AsyncIOScheduler()

    _scheduler.add_job(
        sync_heroes,
        trigger=CronTrigger(hour=3, minute=0),
        id="sync_heroes",
        max_instances=1,
    )

    _scheduler.add_job(
        sync_hero_stats,
        trigger=CronTrigger(hour="*/3", minute=0),
        id="sync_hero_stats",
        max_instances=1,
    )

    _scheduler.start()
    logger.info("스케줄러 시작: sync_heroes(매일 03:00), sync_hero_stats(30분마다)")


def shutdown_scheduler() -> None:
    """스케줄러 종료"""
    global _scheduler
    if _scheduler:
        _scheduler.shutdown()
        _scheduler = None
        logger.info("스케줄러 종료")
