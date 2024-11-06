"""cdek."""
import time
import requests
import json
from typing import List
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from app import models, utils
from app.database import get_db
from app import models
from app.schemas import CityOut

router = APIRouter(tags=['Authentication'])

token_data = {"token": None, "expires_at": 0}

# Configuration
TOKEN_URL = "https://api.edu.cdek.ru/v2/oauth/token?parameters"
GRANT_TYPE = 'client_credentials'
CLIENT_ID = "wqGwiQx0gg8mLtiEKsUinjVSICCjtTEP"
CLIENT_SECRET = "RmAmgvSgSl1yirlz9QupbzOJVqhCxcP5"

DATA = {}
DATA['grant_type'] = GRANT_TYPE
DATA['client_id'] = CLIENT_ID
DATA['client_secret'] = CLIENT_SECRET


async def fetch_token():
    """Fetches a new token from the auth server."""
    response = requests.post(
        TOKEN_URL,
        headers={'content-type': 'application/x-www-form-urlencoded'},
        data=DATA
    )
    response.raise_for_status()
    token_info = response.json()
    token_data["token"] = token_info["access_token"]
    token_data["expires_at"] = time.time() + token_info["expires_in"]


async def get_token():
    """Gets a valid token, refreshing if expired."""
    if not token_data["token"] or token_data["expires_at"] <= time.time():
        print('fetch new token')
        await fetch_token()
    else:
        print('token is not expired')
    return token_data["token"]


@router.get('/cdek')
async def root(_: dict = Depends(get_token)):
    """Check token."""
    return {"message": "CDEK"}


@router.get('/cdek/get_token')
def issue_token(_: Session = Depends(get_db)):
    """Get token."""
    url = "https://api.edu.cdek.ru/v2/oauth/token?parameters"

    data = {}
    data['grant_type'] = 'client_credentials'
    data['client_id'] = 'wqGwiQx0gg8mLtiEKsUinjVSICCjtTEP'
    data['client_secret'] = 'RmAmgvSgSl1yirlz9QupbzOJVqhCxcP5'

    response = requests.post(
        url,
        headers={'content-type': 'application/x-www-form-urlencoded'},
        data=data
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
        }
    )

    if response.status_code == 200:
        data = response.json()
        return {"data": data}
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code,
                            detail='Could not get token')


@router.get('/cdek/get_calculation')
def get_calculation(
    _: Session = Depends(get_db),
    token: dict = Depends(get_token)
):
    """Get token."""
    url = "https://api.edu.cdek.ru/v2/calculator/tarifflist"

    data = {
        'type': 1,
        # 'date': '2020-11-03T11:49:32+0700',
        'currency': 1,
        'lang': 'rus',
        'from_location': {
            'code': 270
        },
        'to_location': {
            'code': 44
        },
        'packages': [
            {
                'height': 10,
                'length': 10,
                'weight': 4000,
                'width': 10
            }
        ]
    }

    response = requests.post(
        url,
        headers={
            'content-type': 'application/json',
            'Authorization': f'Bearer {token}'
        },
        data=json.dumps(data)
    )

    if response.status_code == 200:
        data = response.json()
        return {"data": data}
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code,
                            detail=response.reason)


@router.get('/cdek/get_calculation/{delivery_type}')
def get_calculation_by_type(
    delivery_type: str,
    token: dict = Depends(get_token),
    _: Session = Depends(get_db)
):
    """Get token."""
    url = "https://api.edu.cdek.ru/v2/calculator/tariff"

    data = {
        'type': '1',
        'currency': '1',
        'tariff_code': delivery_type,
        'from_location': {
            'code': 270
        },
        'to_location': {
            'code': 44
        },
        'packages': [
            {
                'height': 10,
                'length': 10,
                'weight': 4000,
                'width': 10
            }
        ]
    }

    response = requests.post(
        url,
        headers={
            'content-type': 'application/json',
            'Authorization': f'Bearer {token}'
        },
        data=json.dumps(data)
    )

    if response.status_code == 200:
        data = response.json()
        return {"data": data}
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code,
                            detail=response.reason)


@router.get('/v1/cdek/get_cities', response_model=List[CityOut])
def get_cities(
    db: Session = Depends(get_db),
    _: dict = Depends(get_token)
):
    """Get cities from database."""

    cities = db.query(models.Cities).all()

    return cities


@router.get('/cdek/store_cities')
def store_cities(
    db: Session = Depends(get_db),
    token: dict = Depends(get_token)
):
    """Store cities in database."""
    url = "https://api.edu.cdek.ru/v2/location/cities"

    response = requests.get(
        url,
        headers={
            'content-type': 'application/x-www-form-urlencoded',
            'Authorization': f'Bearer {token}'
        }
    )

    if response.status_code == 200:
        data = response.json()

        new_cities = [models.Cities(code=city['code'], name=city['city']) for city in data]
        db.add_all(new_cities)
        db.commit()

        # return {"data": data}
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code,
                            detail=response.reason)