import json
import time
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.redis_client import get_redis_client


router = APIRouter(tags=['Root'])


@router.get("/")
async def root(rc: Session = Depends(get_redis_client)):
    result = {"message": "Hello World"}

    value = rc.get('root')
    if not value:
        time.sleep(5)
        value = result
        rc.set('root', json.dumps(result), ex=10)
        return value

    return json.loads(value)
