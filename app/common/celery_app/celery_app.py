import asyncio
from celery import Celery
from celery.signals import (
    worker_shutdown,
    worker_process_init,
)
from kombu import (
    Exchange,
    Queue,
)
from loguru import logger
import nest_asyncio
from tortoise import Tortoise
from typing import Any

from app.common.configs import REDIS_DSN, TORTOISE_ORM
from .scheduler import scheduler_tasks


async def celery_init_orm() -> None:
    logger.info("init tortoise-ORM")
    await Tortoise.init(config=TORTOISE_ORM)
    logger.success("init tortoise-ORM successfully")


async def celery_teardown_orm() -> None:
    logger.info("close tortoise-ORM")
    await Tortoise.close_connections()
    logger.success("close tortoise-ORM successfully")


@worker_process_init.connect()
def init_orm(*args: Any, **kwargs: Any) -> None:
    loop = asyncio.get_event_loop()
    nest_asyncio.apply()
    loop.run_until_complete(celery_init_orm())


@worker_shutdown.connect()
def teardown_orm(*args: Any, **kwargs: Any) -> None:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(celery_teardown_orm())


celery_app = Celery("worker", backend=REDIS_DSN.get('url'), broker=REDIS_DSN.get('url'))
celery_app.conf.enable_utc = False
celery_app.conf.update(
    task_track_started=True,
    timezone="Asia/Ho_Chi_Minh",
)

celery_app.conf.task_queues = ()
celery_app.conf.task_default_queue = "default"
celery_app.conf.task_default_exchange = "default"
celery_app.conf.task_default_exchange_type = "direct"
celery_app.conf.task_default_routing_key = "task"

default_exchange = Exchange("default", type="direct")
celery_app.conf.task_queues = (
    Queue(
        name="default",
        exchange=default_exchange,
        routing_key="task",
    ),
    Queue(
        name="producer",
        exchange=default_exchange,
        routing_key="producer",
    ),
)

celery_app.conf.beat_schedule = scheduler_tasks
