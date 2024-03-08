from confluent_kafka import Consumer, Producer, OFFSET_BEGINNING
from loguru import logger

from app.common.configs import KAFKA_CONFIGS


class KafkaConnector:

    @classmethod
    def init_producer(cls, configs: dict = KAFKA_CONFIGS):
        try:
            logger.info("init a new producer")
            producer = Producer(configs)
            return producer
        except Exception as e:
            logger.error(f"failed to init producer. error: {e}")

    @classmethod
    def init_consumer(cls, configs: dict = KAFKA_CONFIGS):
        try:
            logger.info("init a new consumer")
            consumer = Consumer(configs)
            return consumer
        except Exception as e:
            logger.error(f"failed to init consumer. error: {e}")

    @classmethod
    def _callback(cls, error, message):
        if error:
            logger.error(f"failed to delivery message. error: {error}")
        else:
            logger.debug("delivered event to topic successfully. "
                        f"topic: {message.topic()}. "
                        f"key: {message.key().decode('utf-8')}. "
                        f"value: {message.value().decode('utf-8')}")
