import json
import time
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from aioprometheus.asgi.starlette import metrics

from app.redis_client import get_redis_client


router = APIRouter(tags=['Root'])


@router.get("/")
async def root(rc: Session = Depends(get_redis_client)):
    result = {"message": "Hello World"}

    value = rc.get('root')
    if not value:
        value = result
        rc.set('root', json.dumps(result), ex=10)
        return value

    return json.loads(value)


router.add_route("/metrics", metrics)