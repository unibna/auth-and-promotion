import asyncio
from loguru import logger

from app.common.celery_app import celery_app
from app.promotion.tasks.handlers import sync_auth_events


@celery_app.task(name="sync_auth_events")
def sync_auth_events_task() -> None:
    logger.debug("start syncing auth events")
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(sync_auth_events())
    except Exception as e:
        logger.error(f"failed to sync auth events. error: {e}")
        raise ValueError(e)
    logger.success("sync auth events successfully")
