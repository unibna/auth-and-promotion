import os
import typing
from loguru import logger


def load_redis_config() -> typing.Optional[str]:
    logger.debug("Validate REDIS DNS")
    redis_host = os.getenv("REDIS_HOST")
    redis_port = os.getenv("REDIS_PORT", 6379)
    redis_password = os.getenv("REDIS_PASSWORD")
    if not redis_host and redis_password:
        return {}
    url = f"redis://default:{redis_password}@{redis_host}:{redis_port}/0"
    path = f'default:{redis_password}@{redis_host}:{redis_port}/0'
    return {
        'user': '',
        'password': redis_password,
        'host': redis_host,
        'port': redis_port,
        'path': path,
        'url': url,
    }

# Cache
REDIS_DSN = load_redis_config()

# Database
POSTGRES_CREDENTIALS = {
    "default": {
        "host": os.getenv("POSTGRES_HOST"),
        "port": os.getenv("POSTGRES_PORT"),
        "user": os.getenv("POSTGRES_USER"),
        "password": os.getenv("POSTGRES_PASSWORD"),
        "database": "cake",
    },
}
TORTOISE_ORM = {
    "connections": {
        'default': {
            'engine': 'tortoise.backends.asyncpg',
            'credentials': POSTGRES_CREDENTIALS.get('default')
        },
    },
    "apps": {
        "models": {
            "models": [
                "aerich.models",
                
                "app.auth.models",
                "app.user.models",
                "app.promotion.models",
            ],
            "default_connection": "default",
        }
    }
}

# Kafka
KAFKA_TOPICS = {
    "login_event": "auth.login",
}
KAFKA_CONFIGS = {
    "bootstrap.servers": os.getenv("KAFKA_SERVER"),
    "group.id": os.getenv("KAFKA_GROUP_ID"),
    "auto.offset.reset": os.getenv("KAFKA_AUTO_OFFSET_RESET"),
}

# Security
HASH_PASSWORD_SALT = os.getenv("HASH_PASSWORD_SALT")

# Service
ROOT_URLS = {
    "auth": "http://localhost:8010/auth",
    "user": "http://localhost:8020/users",
    "promotion": "http://localhost:8030/promotion",
}
