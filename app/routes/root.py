from fastapi import APIRouter
from aioprometheus.asgi.starlette import metrics


router = APIRouter(tags=['Root'])


@router.get("/")
async def root():
    result = {"message": "Hello World"}

    return result


router.add_route("/metrics", metrics)
