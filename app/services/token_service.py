# services/token_service.py
import time
import httpx
from fastapi import HTTPException
from app.repositories.token_repository import TokenRepository
from app.core.config import settings


class TokenService:
    def __init__(self, token_repository: TokenRepository):
        self.token_repository = token_repository

    async def get_valid_token(self) -> str:
        """Get a valid token, refreshing if expired."""
        token = await self.token_repository.get_token()

        if not token or self._is_token_expired(token):
            token = await self._fetch_new_token()
            await self.token_repository.save_token(token)

        return token["access_token"]

    def _is_token_expired(self, token: dict) -> bool:
        """Check if the token has expired."""
        return token["expires_at"] <= time.time()

    async def _fetch_new_token(self) -> dict:
        """Fetch a new token from the external service (e.g., CDEK)."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{settings.cdek_endpoint}/v2/oauth/token",
                    data=self._get_token_request_data(),
                    timeout=30
                )
                response.raise_for_status()
                token_info = response.json()
                token_info["expires_at"] = time.time() + token_info["expires_in"]
                return token_info
        except httpx.RequestError as exc:
            raise HTTPException(status_code=500, detail=f"Error fetching new token: {exc}")

    def _get_token_request_data(self) -> dict:
        """Prepare data to request a new token."""
        return {
            "grant_type": settings.cdek_grant_type,
            "client_id": settings.cdek_client_id,
            "client_secret": settings.cdek_client_secret,
        }
