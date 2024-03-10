from datetime import datetime, timedelta
from loguru import logger

from app.common.kafka import KafkaConnector
from app.common.configs import KAFKA_TOPICS
from app.promotion import models, schemas
from app.promotion.configs import KAFKA_CONFIGS


consumer = KafkaConnector.init_consumer(KAFKA_CONFIGS)


async def sync_auth_events():
    consumer.subscribe([KAFKA_TOPICS.get("login_event")])
    message = consumer.poll(1)
    if message:
        logger.warning(f"topic: {message.topic()}")
        logger.warning(f"key: {message.key()}")
        logger.warning(f"value: {message.value()}")


async def process_campaigns():
    campaigns = models.Campaign.filter(
        status__in=[
            models.ValidCampaignStatus.WAITING,
        ],
    ).all()

    for campaign in campaigns:
        to_datetime = datetime.now()
        from_datetime = to_datetime - timedelta(minutes=5)
        if from_datetime <= campaign.start_at and \
                campaign.start_at <= to_datetime:
            await process_campaign(campaign)


async def process_campaign(campaign: models.Campaign):
    logger.info(f"process campaign. campaign_id: {campaign.id}")
    
    # Update to running
    campaign.status = models.ValidCampaignStatus.RUNNING
    await campaign.save()

    # Update to completed
    campaign.status = models.ValidCampaignStatus.COMPLETED
    await campaign.save()
