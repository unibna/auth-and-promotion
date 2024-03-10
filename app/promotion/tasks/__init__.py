from celery.local import PromiseProxy

from app.promotion.tasks import tasks

task_names = []
for k, v in tasks.__dict__.items():
    if isinstance(v, PromiseProxy):
        task_names.append(str(k))

__all__ = [
    *task_names
]
