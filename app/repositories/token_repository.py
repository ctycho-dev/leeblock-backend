import json
from redis.asyncio import Redis
from app.core.logger import get_logger
from typing import Optional

logger = get_logger()


class TokenRepository:

    def __init__(self, cache: Redis):
        self.cache = cache
        self.cache_key = 'cdek_token'

    async def get_token(self) -> Optional[str]:
        """
        Fetch the token from Redis if valid or fetch a new one if expired.
        """
        token = await self.cache.get(self.cache_key)

        if token:
            # If the token is cached, check its expiration time
            return json.loads(token)

        return None

    async def save_token(self, token_data: dict) -> None:
        """Save the token to cache."""
        await self.cache.set(
            self.cache_key,
            json.dumps(token_data),
            ex=token_data['expires_in']
        )


# token_data = {"token": None, "expires_at": 0}


# def get_data_for_token_issue():
#     """Get data for cdek token."""
#     data = {}
#     data['grant_type'] = settings.cdek_grant_type
#     data['client_id'] = settings.cdek_client_id
#     data['client_secret'] = settings.cdek_client_secret

#     return data


# async def fetch_token():
#     """Fetches a new token from the auth server asynchronously."""
#     try:
#         async with httpx.AsyncClient() as client:
#             response = await client.post(
#                 f'{settings.cdek_endpoint}/v2/oauth/token?parameters',
#                 headers={'content-type': 'application/x-www-form-urlencoded'},
#                 data=get_data_for_token_issue(),
#                 timeout=30
#             )
#             response.raise_for_status()
#             token_info = response.json()
#             token_data["token"] = token_info["access_token"]
#             token_data["expires_at"] = time.time() + token_info["expires_in"]
#     except Exception as exc:
#         logger.error('Error in fetch_token: %s', exc)


# async def get_token():
#     """Gets a valid token, refreshing it if expired, asynchronously."""
#     if not token_data["token"] or token_data["expires_at"] <= time.time():
#         await fetch_token()
#     return token_data["token"]