# services/delivery_service.py
import json
import asyncio
import httpx
from typing import Optional

from fastapi import HTTPException

from app.schemas.delivery import DeliveryIn
from app.core.config import settings
from app.services.token_service import TokenService
from app.core.logger import get_logger


logger = get_logger()


class CDEKService:
    def __init__(self, token_service: TokenService):
        self.token_service = token_service

    async def get_calculation_by_type(self, delivery_data: DeliveryIn) -> dict:
        """Get delivery calculation for the given delivery data."""
        token = await self.token_service.get_valid_token()  # Get a valid token

        # Static data for the calculation
        from_city = 137  # Санкт-Петербург
        url = f"{settings.cdek_endpoint}/v2/calculator/tariff"

        tarrif_dict = [
            {'code': 136, 'name': 'Посылка склад-склад'},
            {'code': 137, 'name': 'Посылка склад-дверь'},
            # {'code': 483, 'name': 'Экспресс склад-склад'},
            # {'code': 482, 'name': 'Экспресс склад-дверь'},
            # {'code': 368, 'name': 'Посылка склад-постамат'}
        ]

        data = {
            'type': '1',  # Example: type for calculation
            'from_location': {'code': from_city},
            'to_location': {'code': delivery_data.city_code},
            'packages': [x.model_dump() for x in delivery_data.packages]
        }

        try:
            async with httpx.AsyncClient() as client:
                tasks = [
                    self._make_calculation_request(client, url, data, tariff, token)
                    for tariff in tarrif_dict
                ]
                responses = await asyncio.gather(*tasks)
                return [res for res in responses if res]
        except httpx.RequestError as exc:
            raise HTTPException(status_code=500, detail=f"Error during calculation request: {exc}")

    async def _make_calculation_request(self, client: httpx.AsyncClient, url: str, data: dict, tariff: dict, token: str) -> Optional[dict]:
        """Make a single calculation request."""
        try:
            data['tariff_code'] = str(tariff['code'])
            response = await client.post(
                url,
                headers={
                    'content-type': 'application/json',
                    'Authorization': f'Bearer {token}'
                },
                data=json.dumps(data),
                timeout=30
            )

            if response.status_code == 200:
                return {
                    'name': tariff['name'],
                    'code': tariff['code'],
                    'data': response.json()
                }
        except Exception as exc:
            logger.error('_make_calculation_request: %s', exc)
        return None
