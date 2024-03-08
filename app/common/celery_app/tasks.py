"""
Centralize tasks from the other service modules
"""
from app.common.celery_app.celery_app import celery_app
from app.promotion.tasks import __all__ as promotions_task


__all__ = [
    "celery_app",
    *promotions_task,
]
