from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.core.config import settings
from app.tasks.patent_scanner import run_patent_scanner
from app.tasks.pipeline import run_pipeline
from app.tasks.position_monitor import run_position_monitor
from app.tasks.weekly_digest import run_weekly_digest

scheduler = AsyncIOScheduler(timezone=settings.scheduler_timezone)
PIPELINE_JOB_ID = "daily_scoring_pipeline"
POSITION_MONITOR_JOB_ID = "daily_position_monitor"
PATENT_SCANNER_JOB_ID = "weekly_patent_scanner"
WEEKLY_DIGEST_JOB_ID = "weekly_subscriber_digest"


def start_scheduler() -> None:
    if scheduler.running:
        return

    scheduler.add_job(
        run_pipeline,
        "cron",
        id=PIPELINE_JOB_ID,
        replace_existing=True,
        hour=settings.pipeline_hour_ct,
        minute=0,
    )
    scheduler.add_job(
        run_position_monitor,
        "cron",
        id=POSITION_MONITOR_JOB_ID,
        replace_existing=True,
        hour=settings.position_monitor_hour_ct,
        minute=0,
    )
    scheduler.add_job(
        run_patent_scanner,
        "cron",
        id=PATENT_SCANNER_JOB_ID,
        replace_existing=True,
        day_of_week=settings.patent_scanner_weekday,
        hour=settings.patent_scanner_hour_ct,
        minute=0,
    )
    scheduler.add_job(
        run_weekly_digest,
        "cron",
        id=WEEKLY_DIGEST_JOB_ID,
        replace_existing=True,
        day_of_week=settings.digest_weekday,
        hour=settings.digest_hour_ct,
        minute=0,
    )
    scheduler.start()


def stop_scheduler() -> None:
    if scheduler.running:
        scheduler.shutdown(wait=False)
