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
        minute="*/15", # every fifteen minutes cron style
        second=0, # cron on 0 second
        max_instances=1, # number of concurrent instances
        replace_existing=True, # remove schedule if existing
        jitter=30, # variation of +/- 30 seconds (*:14:30 - *:15:30)
        misfire_grace_time=300, # If not run, what is the variation to rerun
    )
    scheduler.add_job(
        id="simple cron job 2",  # must be a unique name
        func=run_stats,
        trigger="cron",
        second=0, # cron on 0 second
        replace_existing=True, # remove schedule if existing
        
    )
    # example of running interval job at every 10 seconds
    scheduler.add_job(
        id="simple interval",  # must be a unique name
        func=run_addition,
        trigger="interval",
        minutes=5, # every five mintues
        seconds=20, # and 20 seconds
        replace_existing=True, # remove schedule if existing
        jitter=30, # variation in seconds
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

    # if you want to remove a specific job
    scheduler.remove_job("simple cron job 1")
    # if you want to remove all jobs
    scheduler.remove_all_jobs()    
    # shut down scheduler on closure
    scheduler.shutdown()
