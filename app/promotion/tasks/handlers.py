from loguru import logger

from app.common.kafka import KafkaConnector
from app.common.configs import KAFKA_TOPICS
from app.promotion.configs import KAFKA_CONFIGS


consumer = KafkaConnector.init_consumer(KAFKA_CONFIGS)


async def sync_auth_events():
    consumer.subscribe([KAFKA_TOPICS.get("login_event")])
    message = consumer.poll(1)
    if message:
        logger.warning(f"topic: {message.topic()}")
        logger.warning(f"key: {message.key()}")
        logger.warning(f"value: {message.value()}")
