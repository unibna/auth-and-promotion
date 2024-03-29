from celery.schedules import crontab, schedule


scheduler_tasks = {
    "trigger_campaigns": {
        "task": "trigger_campaigns",
        "schedule": schedule(run_every=1),
    },
    "trigger_running_campaigns": {
        "task": "trigger_running_campaigns",
        "schedule": schedule(run_every=0.5),
    },
}
