"""APScheduler jobs (section 10). Deterministic orchestration."""
from __future__ import annotations

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger


def daily_digest_job() -> None:
    raise NotImplementedError("Pull recent messages, cluster, summarize, persist")


def reembed_backfill_job() -> None:
    raise NotImplementedError("Re-embed messages whose embedding model version changed")


def graph_refresh_job() -> None:
    raise NotImplementedError("Refresh frequent-contact and topic edges from last N days")


def build_scheduler() -> BackgroundScheduler:
    sched = BackgroundScheduler()
    sched.add_job(daily_digest_job, CronTrigger(hour=7, minute=0), id="daily_digest")
    sched.add_job(graph_refresh_job, CronTrigger(hour=3, minute=0), id="graph_refresh")
    return sched
