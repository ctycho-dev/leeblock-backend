"""Create app."""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import cdek, email, db
from app.redis_client import redis_client
from app.config.logger import get_logger


logger = get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastApi lifecycle."""

    yield

    redis_client.close()


def create_app() -> FastAPI:
    """Create FastApi application."""

    app = FastAPI(lifespan=lifespan)

    logger.info('Start application')

    origins = [
        "https://leeblock.ru",
        "https://drive-t.ru",
        "https://wwww.leeblock.ru",
        "https://wwww.drive-t.ru",
        # "http://localhost:3000",
        # "http://localhost:5123"
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(cdek.router)
    app.include_router(email.router)
    app.include_router(db.router)

    return app
