"""
Centralize tasks from the other service modules
"""
from app.common.celery_app.celery_app import celery_app
from app.promotion.tasks import __all__ as promotion_tasks
from app.common.producers import produce_event_task


__all__ = [
    "celery_app",
    *promotion_tasks,

    "produce_event_task",
]
