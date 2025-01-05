"""cdek."""
import time
import json
import asyncio
import httpx
from fastapi import Response, status, HTTPException, Depends, APIRouter

from app.schemas.delivery import DeliveryIn
from app.services.token_service import TokenService
from app.services.cdek_service import CDEKService
from app.repositories.token_repository import TokenRepository
from app.core.logger import get_logger
from app.dependencies.injection import DependencyFactory
from app.dependencies.injection import get_factory
from app.core.config import settings

logger = get_logger()

router = APIRouter(
    prefix='/delivery',
    tags=['Delivery']
)


@router.post('/calculate')
async def get_calculation_by_type(
    delivery_data: DeliveryIn,
    factory: DependencyFactory = Depends(get_factory)
):
    """Get token."""
    try:
        token_repo = TokenRepository(factory.cache)
        token_service = TokenService(token_repo)
        cdek_service = CDEKService(token_service)

        response_data = await cdek_service.get_calculation_by_type(delivery_data)

        return response_data
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching token: {exc}"
        ) from exc
    

    # from_city = 137  # Санкт-Петербург
    # url = f"{settings.cdek_endpoint}/v2/calculator/tariff"
    # response_data = []

    # tarrif_dict = [
    #     {'code': 136, 'name': 'Посылка склад-склад'},
    #     # {'code': 483, 'name': 'Экспресс склад-склад'},
    #     {'code': 137, 'name': 'Посылка склад-дверь'},
    #     # {'code': 482, 'name': 'Экспресс склад-дверь'},
    #     # {'code': 368, 'name': 'Посылка склад-постамат'}
    # ]

    # data = {
    #     'type': '1',
    #     # 'tariff_code': delivery_type,
    #     'from_location': {
    #         'code': from_city
    #     },
    #     'to_location': {
    #         'code': delivery_data.city_code
    #     },
    #     'packages': [x.model_dump() for x in delivery_data.packages]
    # }

    # async with httpx.AsyncClient() as client:
    #     tasks = []
    #     for tarrif in tarrif_dict:
    #         data['tariff_code'] = str(tarrif['code'])

    #         task = client.post(
    #             url,
    #             headers={
    #                 'content-type': 'application/json',
    #                 'Authorization': f'Bearer {token}'
    #             },
    #             data=json.dumps(data),
    #             timeout=30
    #         )
    #         tasks.append(task)

    #     responses = await asyncio.gather(*tasks)

    # for tarrif, response in zip(tarrif_dict, responses):
    #     try:
    #         if response.status_code == 200:
    #             response_data.append({
    #                 'name': tarrif['name'],
    #                 'code': tarrif['code'],
    #                 'data': response.json()
    #             })
    #     except Exception as exc:  # ignore: W0718:broad-exception-caught
    #         logger.error('Error in processing tariff %s: %s', tarrif["name"], exc)

    # return response_data


# @router.get('/get_cdek_token')
# def issue_token():
#     """Get token."""

#     data = get_data_for_token_issue()

#     response = requests.post(
#         f'{settings.cdek_endpoint}/v2/oauth/token?parameters',
#         headers={'content-type': 'application/x-www-form-urlencoded'},
#         data=data,
#         timeout=30
#     )

#     if response.status_code == 200:
#         data = response.json()
#         return {"data": data}
#     if response.status_code != 200:
#         raise HTTPException(status_code=response.status_code,
#                             detail='Could not get token')


# @router.get('/cdek/get_locations/{city}/{code}')
# def get_locations(
#     city: str,
#     code: str,
#     token: dict = Depends(get_token),
# ):
#     """Get locations by city name."""
#     url = f"https://api.cdek.ru/v2/location/suggest/cities?name={city}&country_code={code}"

#     response = requests.get(
#         url,
#         headers={
#             'content-type': 'application/json',
#             'Authorization': f'Bearer {token}'
#         },
#         timeout=30
#     )

#     if response.status_code == 200:
#         data = response.json()
#         return {"data": data}
#     if response.status_code != 200:
#         raise HTTPException(status_code=response.status_code,
#                             detail='Could not get locations')
