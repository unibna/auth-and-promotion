from celery.schedules import crontab
from datetime import timedelta


scheduler_tasks = {
    "sync_auth_events": {
        "task": "sync_auth_events",
        "schedule": crontab(minute="*")
    },
}