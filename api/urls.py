from fastapi import FastAPI
from api.rpa_job import router as rpa_job_router


def register_routers(app: FastAPI):
    """
    注册路由
    """
    app.include_router(rpa_job_router, prefix="/api", tags=["RPA Job"])
