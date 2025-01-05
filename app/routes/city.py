"""City router."""
import os
import requests
import json
from typing import List
from fastapi import HTTPException, Depends, APIRouter, status
from sqlalchemy.future import select

from app.models.city import City
from app.schemas.delivery import CityOut
from app.repositories.city_repository import CityRepository
from app.dependencies.factory import DependencyFactory
from app.core.logger import get_logger
from app.dependencies.injection import get_factory

CACHE_TTL = int(os.getenv("CACHE_TTL", 86400))
logger = get_logger()

router = APIRouter(
    prefix='/cities',
    tags=['City']
)


@router.get('/', response_model=List[CityOut])
async def get_cities(
    factory: DependencyFactory = Depends(get_factory)
):
    """Gey cities."""
    try:
        cache_key = 'cities_cdek'

        cached_cities = await factory.cache.get(cache_key)
        if cached_cities:
            return json.loads(cached_cities)
        
        city_repo = CityRepository(factory.db)
        cities = await city_repo.get_by_sequence()

        cities_list = [
            CityOut.model_validate(city).model_dump()
            for city in cities
        ]

        await factory.cache.set(cache_key, json.dumps(cities_list), ex=CACHE_TTL)

        return cities_list
    except Exception as exc:
        logger.error('get: /cities %s', exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while processing your request."
        ) from exc


# ======================================
# DELETE below
# ======================================


@router.get('/v1/cdek/get_cities', response_model=List[CityOut])
async def get_city(
    factory: DependencyFactory = Depends(get_factory)
):
    """Get cities from database with caching."""
    cache_key = 'cities_cdek'
    
    try:
        # Fetch from the database
        result = await factory.db.execute(select(City).order_by(City.sequence))
        cities = result.scalars().all()
        # cities = db.query(Cities).order_by(Cities.sequence).all()
        product_list = [CityOut.model_validate(city).dict() for city in cities]
        
        # Attempt to cache the result
        try:
            factory.cache.set(cache_key, json.dumps(product_list), ex=86400)
        except Exception as redis_exc:  # pylint: disable=W0718
            logger.error(f"Failed to set Redis cache: {redis_exc}")
        return product_list
    except Exception as db_exc:  # pylint: disable=W0718
        logger.error(f"Database error: {db_exc}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while fetching cities. Please try again later."
        ) from db_exc


# @router.get('/cdek/store_cities')
# def store_cities(
#     db: Session = Depends(get_db),
#     token: dict = Depends(get_token)
# ):
#     """Store cities in database."""
#     url = f"{settings.cdek_endpoint}/v2/location/cities"

#     response = requests.get(
#         url,
#         headers={
#             'content-type': 'application/x-www-form-urlencoded',
#             'Authorization': f'Bearer {token}'
#         },
#         timeout=30
#     )

#     if response.status_code == 200:
#         data = response.json()

#         new_cities = [Cities(code=city['code'], name=city['city']) for city in data]
#         db.add_all(new_cities)
#         db.commit()

#     if response.status_code != 200:
#         raise HTTPException(status_code=response.status_code,
#                             detail=response.reason)