import os
from common.logger import logger
from common import register_docs
from common.database import register_db
from fastapi import FastAPI
from conf.config import settings

from middleware.cors import register_cors_middleware
from api.urls import register_routers

app = FastAPI(
    description=settings.DESC,
    version=settings.VERSION,
    docs_url=None,
    redoc_url=None

)


# 使用本地docs静态文件
register_docs(app)

# 注册中间件
register_cors_middleware(app)

# 数据库初始化
register_db(app)


# 注册路由
register_routers(app)





if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="localhost",
        port=settings.PORT,
        reload=True,
        log_level="debug" if settings.DEBUG else "info"
    )