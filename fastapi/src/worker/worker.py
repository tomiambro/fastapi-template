import random

from celery import Celery
from celery.schedules import crontab
from settings import data, logger_for

from .tasks import sum

logger = logger_for(__name__)


class Config:
    broker_url = data.get("celery_broker_url")
    # List of modules to import when the Celery worker starts.
    imports = ("worker.tasks",)
    enable_utc = True
    timezone = "America/New_York"


worker = Celery("fastapi")
worker.config_from_object(Config)


@worker.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    # Executes every 15 seconds
    # sender.add_periodic_task(
    #     15.0, sum.s(random.randint(1, 10), random.randint(1, 10)), expires=10
    # )
    # Executes every day morning at 12 a.m.
    sender.add_periodic_task(
        crontab(hour=12),
        sum.s(random.randint(1, 10), random.randint(1, 10)),
    )
