from fastapi import FastAPI
from loguru import logger
from tortoise.contrib.fastapi import register_tortoise

from app.common import configs


def init(app: FastAPI, service_name: str) -> None:
    logger.info(f"init service: {service_name}")
    init_orm(app, service_name)
    logger.success(f"init service: {service_name} successfully")


def init_orm(app: FastAPI, service_name: str = None) -> None:
    logger.info("init ORM")
    register_tortoise(app, config=configs.TORTOISE_ORM)
    logger.success("init ORM successfully")
