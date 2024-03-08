import os


SERVICE_NAME = "promotion"
API_SERVER_INFO = {
    "host": os.getenv("PROMOTION_API_SERVICE_HOST"),
    "port": int(os.getenv("PROMOTION_API_SERVICE_PORT")),
    "prefix": "/promotions",
}

# Kafka
KAFKA_CONFIGS = {
    "bootstrap.servers": os.getenv("KAFKA_SERVER"),
    "group.id": "promotion_service",
    "auto.offset.reset": os.getenv("KAFKA_AUTO_OFFSET_RESET"),
}
