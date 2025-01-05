import hashlib
import json
import httpx
from app.models.request import Request
from app.schemas.payment import CheckoutIn
from app.repositories.request_repository import RequestRepository
from app.core.config import settings
from fastapi import HTTPException, status


class PaymentService:

    def generate_token(self, data, request_id):
        """Generate SHA-256 token for the payment."""
        try:
            data_for_token = [
                str(data.Amount),
                settings.terminal_desc,
                str(request_id),
                settings.terminal_pwd,
                settings.terminal_key
            ]
            data_string = ''.join(data_for_token)
            sha256_hash = hashlib.sha256(data_string.encode('utf-8')).hexdigest()
            return sha256_hash
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to generate token: {exc}"
            ) from exc

    async def call_tinkoff_api(
            self,
            data: CheckoutIn,
            request_id: int,
            sha256_hash: str
    ):
        """Send a request to Tinkoff API to initiate payment."""

        init_data = {
            'TerminalKey': settings.terminal_key,
            'Amount': data.Amount,
            'OrderId': request_id,
            'Description': settings.terminal_desc,
            'Token': sha256_hash,
            'DATA': data.DATA.model_dump(),
            'Receipt': data.Receipt.model_dump()
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f'{settings.tinkoff_url}/v2/Init',
                    headers={'Content-Type': 'application/json'},
                    json=init_data,
                    timeout=30
                )
                response.raise_for_status()
            except httpx.RequestError as exc:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to connect to payment provider: {exc}"
                ) from exc
            except httpx.HTTPStatusError as exc:
                raise HTTPException(
                    status_code=exc.response.status_code,
                    detail=f"Payment provider returned an error: {exc}"
                ) from exc
            return response
