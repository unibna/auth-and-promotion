import json
from loguru import logger
from time import time

from app.auth.configs import KAFKA_CONFIGS
from app.auth.schemas import Session
from app.common.kafka import KafkaConnector
from app.common.configs import KAFKA_TOPICS


kafka_producer = KafkaConnector.init_producer(KAFKA_CONFIGS)


async def product_login_event(session: Session) -> None:
    try:
        kafka_producer.produce(
            topic=KAFKA_TOPICS.get("login_event"),
            key=f"{session.id}_{int(time())}",
            value=json.dumps(session.data).encode(),
        )
        kafka_producer.poll(1)
        kafka_producer.flush()
    except Exception as e:
        logger.error(f"failed to produce login event. error: {e}")
