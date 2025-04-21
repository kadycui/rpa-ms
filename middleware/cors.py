from fastapi import FastAPI
from conf.config import settings
from fastapi.middleware.cors import CORSMiddleware

def register_cors_middleware(app: FastAPI):
    app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.CORS_ORIGINS,  # Allow all origins
            allow_credentials=True,
            allow_methods=["*"],  # Allow all methods
            allow_headers=["*"],  # Allow all headers
        )