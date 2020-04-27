# -*- coding: utf-8 -*-
from datetime import date

from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import utc

from math_func import happy_fourth, run_addition, run_stats

jobstores = {"default": SQLAlchemyJobStore(url="sqlite:///app.db")}

executors = {"default": AsyncIOExecutor()}

job_defaults = {"coalesce": False, "max_instances": 20, "misfire_grace_time": 3600}

scheduler = AsyncIOScheduler()

scheduler.configure(
    jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc
)


def start_jobs():

    # example of running cron job at 0 and 30 second mark
    scheduler.add_job(
        id="simple cron job 1",  # must be a unique name
        func=run_stats,
        trigger="cron",
        second=0,
        max_instances=3,
        replace_existing=True,  # prevents issue when app restarts
    )
    scheduler.add_job(
        id="simple cron job 2",  # must be a unique name
        func=run_stats,
        trigger="cron",
        second=0,
        max_instances=3,
        replace_existing=True,  # prevents issue when app restarts
    )
    # example of running interval job at every 10 seconds
    scheduler.add_job(
        id="simple interval",  # must be a unique name
        func=run_addition,
        trigger="interval",
        seconds=10,
        max_instances=3,
        replace_existing=True,  # prevents issue when app restarts
    )

    # example of running a job on a specific date
    scheduler.add_job(
        id="happy fourth",  # must be a unique name
        func=happy_fourth,
        trigger="date",
        run_date=date(2020, 7, 4),  # date to run
        max_instances=3,
        replace_existing=True,  # prevents issue when app restarts
    )
    scheduler.start()


def shut_down_schedule():

    scheduler.remove_job("simple cron job 1")
    scheduler.remove_job("simple cron job 2")
    scheduler.remove_job("simple interval")
    scheduler.remove_job("happy fourth")
    scheduler.shutdown()
