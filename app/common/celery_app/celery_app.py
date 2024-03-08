from celery import Celery
from kombu import (
    Exchange,
    Queue,
)

from app.common.configs import REDIS_DSN
from .scheduler import scheduler_tasks


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
)

celery_app.conf.beat_schedule = scheduler_tasks
