"""cdek."""
import time
import requests
import json
from typing import List
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from app import models, utils
from app.database import get_db
from app.config.config import settings
from app import models
from app.schemas import CityOut, DeliveryIn
from app.redis_client import get_redis_client
from app.config.logger import get_logger

logger = get_logger()

router = APIRouter(tags=['Authentication'])

token_data = {"token": None, "expires_at": 0}


def get_data_for_token_issue():
    """Get data for cdek token."""
    data = {}
    data['grant_type'] = settings.cdek_grant_type
    data['client_id'] = settings.cdek_client_id
    data['client_secret'] = settings.cdek_client_secret

    return data


async def fetch_token():
    """Fetches a new token from the auth server."""
    try:
        response = requests.post(
            f'{settings.cdek_endpoint}/v2/oauth/token?parameters',
            headers={'content-type': 'application/x-www-form-urlencoded'},
            data=get_data_for_token_issue(),
            timeout=30
        )

        response.raise_for_status()
        token_info = response.json()
        token_data["token"] = token_info["access_token"]
        token_data["expires_at"] = time.time() + token_info["expires_in"]

    except Exception as exc:  # pylint: disable=W0718
        logger.error('Error: fetch_token %s', exc)


async def get_token():
    """Gets a valid token, refreshing if expired."""
    if not token_data["token"] or token_data["expires_at"] <= time.time():
        await fetch_token()
    return token_data["token"]


@router.get('/cdek')
async def root(_: dict = Depends(get_token)):
    """Check token."""
    return {"message": "CDEK"}


@router.get('/cdek/get_token')
def issue_token(_: Session = Depends(get_db)):
    """Get token."""

    data = get_data_for_token_issue()
    print(data)

    response = requests.post(
        f'{settings.cdek_endpoint}/v2/oauth/token?parameters',
        headers={'content-type': 'application/x-www-form-urlencoded'},
        data=data,
        timeout=30
    )

    if response.status_code == 200:
        data = response.json()
        return {"data": data}
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code,
                            detail='Could not get token')


@router.get('/cdek/get_locations/{city}/{code}')
def get_locations(
    city: str,
    code: str,
    token: dict = Depends(get_token),
    _: Session = Depends(get_db)
):
    """Get locations by city name."""
    url = f"https://api.cdek.ru/v2/location/suggest/cities?name={city}&country_code={code}"

    response = requests.get(
        url,
        headers={
            'content-type': 'application/json',
            'Authorization': f'Bearer {token}'
        },
        timeout=30
    )

    if response.status_code == 200:
        data = response.json()
        return {"data": data}
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code,
                            detail='Could not get locations')


# @router.get('/cdek/get_calculation')
# def get_calculation(
#     _: Session = Depends(get_db),
#     token: dict = Depends(get_token)
# ):
#     """Get shipping calculation from CDEK."""

#     url = f"{settings.cdek_endpoint}/v2/calculator/tarifflist"

#     data = {
#         'type': 1,
#         'currency': 1,
#         'lang': 'rus',
#         'from_location': {
#             'code': 270  # Example location code, adjust as needed
#         },
#         'to_location': {
#             'code': 44  # Example destination location code, adjust as needed
#         },
#         'packages': [
#             {
#                 'height': 10,
#                 'length': 10,
#                 'weight': 4000,  # Example package weight (grams)
#                 'width': 10
#             }
#         ]
#     }

#     try:
#         response = requests.post(
#             url,
#             headers={
#                 'content-type': 'application/json',
#                 'Authorization': f'Bearer {token}'
#             },
#             data=json.dumps(data),
#             timeout=30
#         )

#         response.raise_for_status()

#         return {"data": response.json()}

#     except requests.exceptions.RequestException as exc:
#         raise HTTPException(
#             status_code=500,
#             detail=f"An error occurred while fetching calculation data: {exc}"
#         )
#     except ValueError as exc:
#         raise HTTPException(
#             status_code=500,
#             detail=f"Error parsing response: {exc}"
#         )


@router.post('/v1/cdek/get_calculation')
def get_calculation_by_type(
    delivery_data: DeliveryIn,
    token: dict = Depends(get_token),
    _: Session = Depends(get_db)
):
    """Get token."""
    from_city = 137  # Санкт-Петербург
    url = f"{settings.cdek_endpoint}/v2/calculator/tariff"
    response_data = []

    tarrif_dict = [
        {'code': 136, 'name': 'Посылка склад-склад'},
        # {'code': 483, 'name': 'Экспресс склад-склад'},
        {'code': 137, 'name': 'Посылка склад-дверь'},
        # {'code': 482, 'name': 'Экспресс склад-дверь'}
        # {'code': 368, 'name': 'Посылка склад-постамат'}
    ]

    data = {
        'type': '1',
        # 'tariff_code': delivery_type,
        'from_location': {
            'code': from_city
        },
        'to_location': {
            'code': delivery_data.city_code
        },
        'packages': [x.model_dump() for x in delivery_data.packages]
    }

    for tarrif in tarrif_dict:
        try:
            data['tariff_code'] = str(tarrif['code'])

            response = requests.post(
                url,
                headers={
                    'content-type': 'application/json',
                    'Authorization': f'Bearer {token}'
                },
                data=json.dumps(data),
                timeout=30
            )

            if response.status_code == 200:
                response_data.append({
                    'name': tarrif['name'],
                    'code': tarrif['code'],
                    'data': response.json()
                })
        except Exception as exc:  # ignore: W0718:broad-exception-caught
            print(f'Error /v1/cdek/get_calculation: {exc}')

    return response_data


@router.get('/v1/cdek/get_cities', response_model=List[CityOut])
def get_cities(
    db: Session = Depends(get_db),
    rc: Session = Depends(get_redis_client)
):
    """Get cities from database with caching."""
    cache_key = 'cities_cdek'
    
    try:
        # Attempt to fetch from Redis
        cached_cities = rc.get(cache_key)
        if cached_cities:
            return json.loads(cached_cities)
    except Exception as redis_exc:  # pylint: disable=W0718
        logger.error(f"Redis error: {redis_exc}")

    try:
        # Fetch from the database
        cities = db.query(models.Cities).order_by(models.Cities.sequence).all()
        product_list = [CityOut.model_validate(city).dict() for city in cities]
        
        # Attempt to cache the result
        try:
            rc.set(cache_key, json.dumps(product_list), ex=86400)
        except Exception as redis_exc:  # pylint: disable=W0718
            logger.error(f"Failed to set Redis cache: {redis_exc}")
        
        return product_list
    except Exception as db_exc:  # pylint: disable=W0718
        logger.error(f"Database error: {db_exc}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while fetching cities. Please try again later."
        ) from db_exc


@router.get('/cdek/store_cities')
def store_cities(
    db: Session = Depends(get_db),
    token: dict = Depends(get_token)
):
    """Store cities in database."""
    url = f"{settings.cdek_endpoint}/v2/location/cities"

    response = requests.get(
        url,
        headers={
            'content-type': 'application/x-www-form-urlencoded',
            'Authorization': f'Bearer {token}'
        },
        timeout=30
    )

    if response.status_code == 200:
        data = response.json()

        new_cities = [models.Cities(code=city['code'], name=city['city']) for city in data]
        db.add_all(new_cities)
        db.commit()

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code,
                            detail=response.reason)
