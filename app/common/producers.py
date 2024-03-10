import asyncio
import json
from loguru import logger
from typing import Any, Union
from uuid import uuid4

from app.common.celery_app import celery_app
from app.common.configs import KAFKA_CONFIGS
from app.common.kafka import KafkaConnector


kafka_producer = KafkaConnector.init_producer(KAFKA_CONFIGS)


@celery_app.task(routing_key="producer", exchange="default", name="produce_event_task")
def produce_event_task(
    topic: str,
    value: Any,
    key: Union[int, str] = None,
) -> None:
    logger.info("produce event")
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(produce_event(topic, value, key))
    except Exception as e:
        logger.error(f"failed to produce event. error: {e}")
        raise ValueError(e)
    logger.success("produce event successfully")


async def produce_event(
    topic: str,
    value: Any,
    key: Union[int, str] = None,
) -> None:
    try:
        if not key:
            key = str(uuid4())
            value['id'] = key
        if not isinstance(value, bytes):
            value = json.dumps(value).encode()
        payload = {
            "topic": topic,
            "key": key,
            "value": value,
        }
        logger.debug(f"produce message. payload: {payload}")
        kafka_producer.produce(**payload)
        kafka_producer.poll(1)
        kafka_producer.flush()
    except Exception as e:
        logger.error(f"failed to produce login event. error: {e}")

