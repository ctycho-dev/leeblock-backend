"""Create app."""
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.routes import root
from app.routes import delivery
from app.routes import email
from app.routes import product
from app.routes import requests
from app.routes import payment
from app.routes import user
from app.routes import city
from app.redis_client import redis_client
from app.core.logger import get_logger
from app.metrics import request_counter
from app.metrics import response_counter
from app.metrics import response_histogram

logger = get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastApi lifecycle."""

    yield

    try:
        await redis_client.close()
        await redis_client.connection_pool.disconnect()
    except Exception as e:
        print(f"Error during Redis shutdown: {e}")


def create_app() -> FastAPI:
    """Create FastApi application."""

    app = FastAPI(lifespan=lifespan)

    logger.info('Start application')

    origins = [
        "https://wwww.leeblock.ru",
        "http://localhost:3000",
        "http://localhost:3001",
    ]

    @app.middleware("http")
    async def dynamic_cors_middleware(request: Request, call_next):
        start_time = time.time()
        endpoint = request.url.path
        # origin = request.headers.get("origin")
        
        request_counter.inc({"path": endpoint})

        response = await call_next(request)

        elapsed_time = time.time() - start_time

        response_histogram.observe({"path": endpoint}, elapsed_time)
        response_counter.inc({"path": endpoint, "state": response.status_code})

        # Check if the origin is allowed
        # if origin in origins:
        #     response.headers["Access-Control-Allow-Origin"] = origin
        #     response.headers["Access-Control-Allow-Credentials"] = "true"
        #     response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        #     response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"

        return response

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(delivery.router)
    app.include_router(email.router)
    app.include_router(product.router)
    app.include_router(requests.router)
    app.include_router(payment.router)
    app.include_router(root.router)
    app.include_router(user.router)
    app.include_router(city.router)

    return app
