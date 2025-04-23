from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from loguru import logger
from tortoise import Tortoise
from conf.config import settings


db_config = {
    'connections': {
        'default': {
            'engine': f'tortoise.backends.{settings.MYSQL_ENGINE}',
            'credentials': {
                'host': f'{settings.MYSQL_HOST}',
                'port': f'{settings.MYSQL_PORT}',
                'user': f'{settings.MYSQL_USER}',
                'password': f'{settings.MYSQL_PASSWORD}',
                'database': f'{settings.MYSQL_DATABASE}',
                'charset': f'{settings.MYSQL_ENCODING}',
                'echo': f'{settings.MYSQL_ECHO}'
            }
        },
    },
    'apps': {
        'models': {
            'models': [
                "models.rpa"
            ],
            'default_connection': 'default',
        },
    },
    'use_tz': False,
    'timezone': 'Asia/Shanghai'
}


def register_db(app: FastAPI) -> None:
    register_tortoise(
        app,
        config=db_config,
        generate_schemas=settings.GENERATE_SCHEMAS,
        add_exception_handlers=settings.MYSQL_ADD_EXCEPTION_HANDLERS
    )
    logger.info(f"数据库连接成功: {settings.MYSQL_HOST}:{settings.MYSQL_PORT}/{settings.MYSQL_DATABASE}")
