import asyncio
from celery.signals import worker_init
from datetime import datetime, timedelta, timezone
import json
from loguru import logger
from tortoise.expressions import Q
from typing import List

from app.common.celery_app import celery_app
from app.common.configs import KAFKA_TOPICS
from app.common.kafka import KafkaConnector
from app.promotion import models, schemas
from app.promotion.configs import KAFKA_CONFIGS


@celery_app.task(name="trigger_campaigns")
def trigger_campaigns_task() -> None:
    logger.info("trigger campaigns")
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(trigger_campaigns())
    except Exception as e:
        logger.error(f"failed to trigger campaigns. error: {e}")
        raise ValueError(e)
    logger.success("trigger campaigns successfully")


@celery_app.task(name="trigger_running_campaigns")
def trigger_running_campaigns_task() -> None:
    logger.info("trigger RUNNING campaigns")
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(trigger_running_campaigns())
    except Exception as e:
        logger.error(f"failed to trigger RUNNING campaigns. error: {e}")
        raise ValueError(e)
    logger.success("trigger RUNNING campaigns successfully")


@celery_app.task(name="process_running_campaign")
def process_running_campaign_task(campaign_id: int) -> None:
    logger.info("process RUNNING campaigns")
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(process_running_campaign(campaign_id))
    except Exception as e:
        logger.error(f"failed to process RUNNING campaigns. error: {e}")
        raise ValueError(e)
    logger.success("process RUNNING campaigns successfully")


async def trigger_campaigns():
    campaigns = await models.Campaign.filter(
        Q(status__in=[
            models.ValidCampaignStatus.WAITING,
        ]) \
        & (
            Q(start_at__gte=(datetime.utcnow() - timedelta(minutes=5)))
            | Q(start_at__lte=datetime.utcnow())
        )
    ).all()
    logger.info(f"trigger campaigns. total WAITING campaign: {len(campaigns)}")

    for campaign in campaigns:
        logger.debug("check to trigger campaign. "
                    f"campaign: {campaign.id}. "
                    f"scheduler: [{campaign.start_at}:{campaign.end_at}].")
        to_datetime = datetime.now().replace(tzinfo=timezone.utc)
        from_datetime = to_datetime - timedelta(minutes=5)
        if from_datetime <= campaign.start_at and \
                campaign.start_at <= to_datetime:
            process_running_campaign_task.apply_async(
                kwargs={'campaign_id': campaign.id},
            )


async def trigger_running_campaigns():
    campaigns = await models.Campaign.filter(
        Q(status__in=[
            models.ValidCampaignStatus.RUNNING,
        ]) \
        & (
            Q(end_at__isnull=True) \
            | Q(end_at__gte=datetime.utcnow())
        )
    ).all()
    logger.info(f"trigger campaigns. total RUNNING campaigns: {len(campaigns)}")

    for campaign in campaigns:
        process_running_campaign_task.apply_async(
            kwargs={"campaign_id": campaign.id},
        )


async def process_running_campaign(
        campaign_id: int,
        events_topics: List[str] = [KAFKA_TOPICS.get('user_events')],
) -> None:
    logger.info(f"process RUNNING campaign. campaign_id: {campaign_id}")
    campaign = await models.Campaign.get(id=campaign_id)
    if not campaign:
        logger.error(f"campaign is not found. campaign_id: {campaign_id}")
        return

    if campaign.status is not models.ValidCampaignStatus.RUNNING:
        logger.debug(f"update campaign's status to RUNNING. campaign_id: {campaign_id}")
        await models.Campaign.get(id=campaign_id).update(
            status=models.ValidCampaignStatus.RUNNING,
        )
        
    consumer = KafkaConnector.init_consumer(KAFKA_CONFIGS)
    consumer.subscribe(events_topics)
    message = consumer.poll(1.0)
    if message:
        message_value = json.loads(message.value().decode())
        logger.debug(f"-----> message_value. type: {type(message_value)}. value: {message_value}")
        if message_value.get("action_type") == "USER_ACTIVATE":
            logger.warning("************issue voucher for a new user************")
    else:
        logger.warning(f"there is no message to process. campaign_id: {campaign_id}")
    consumer.close()    

    logger.success(f"process RUNNING campaign successfully. campaign_id: {campaign_id}")
