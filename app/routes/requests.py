import json
import os
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.request_repository import RequestRepository
from app.schemas.requests import RequestsResponse
from app.dependencies.factory import DependencyFactory
from app.core.logger import get_logger
from app.dependencies.injection import get_current_user
from app.dependencies.injection import get_factory


router = APIRouter(
    tags=['Requests'],
    prefix='/requests'
)

logger = get_logger()

# Cache TTL (configurable via environment variable)
CACHE_TTL = int(os.getenv("CACHE_TTL", 300))


@router.get('/')
async def get_requests(
    factory: DependencyFactory = Depends(get_factory),
    _: AsyncSession = Depends(get_current_user)
):
    """Get all requests."""
    try:
        cache_key = 'request_list'

        cached_products = await factory.cache.get(cache_key)
        if cached_products:
            return json.loads(cached_products)

        request_repo = RequestRepository(factory.db)
        requests = await request_repo.get_all()

        request_list = [
            RequestsResponse.model_validate(request).model_dump()
            for request in requests
        ]

        await factory.cache.set(cache_key, json.dumps(request_list), ex=CACHE_TTL)

        return request_list
    except Exception as exc:
        logger.error('/requests %s', exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while processing your request."
        ) from exc


@router.get('/{request_id}')
async def get_request_by_id(
    request_id: int,
    factory: DependencyFactory = Depends(get_factory),
    _: AsyncSession = Depends(get_current_user)
):
    """Get a request by ID."""
    try:
        cache_key = f'request:{request_id}'

        cached_product = await factory.cache.get(cache_key)
        if cached_product:
            return json.loads(cached_product)

        request_repo = RequestRepository(factory.db)
        request = await request_repo.get_by_id(request_id)

        if not request:
            return None

        request_json = RequestsResponse.model_validate(request).model_dump()
        
        await factory.cache.set(cache_key, json.dumps(request_json), ex=CACHE_TTL)

        return request
    except Exception as exc:
        logger.error('/requests/%s %s', request_id, exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while processing your request."
        ) from exc
