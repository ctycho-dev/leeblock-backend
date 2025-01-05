import os
import json
from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from app.services.email_service import EmailService
from app.repositories.user_repository import UserRepository
from app.repositories.token_repository import TokenRepository
from app.dependencies.factory import DependencyFactory
from app.schemas.users import UserOut
from app.db.database import get_db
from app.redis_client import get_redis_client
from app.utils.oauth2 import verify_access_token


CACHE_TTL = int(os.getenv("CACHE_TTL", 900))
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


def get_email_service() -> EmailService:
    """Provide an instance of the EmailService."""
    return EmailService()


def get_factory(
    db: AsyncSession = Depends(get_db),
    rc: Redis = Depends(get_redis_client),
) -> DependencyFactory:
    """Get factory instance."""
    return DependencyFactory(db=db, cache=rc)


def get_token_service(
    redis: Redis = Depends(get_redis_client)
) -> TokenRepository:
    return TokenRepository(redis)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    factory: DependencyFactory = Depends(get_factory)
):
    """Get current user from token with caching."""
    
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail='Could not validate credentials',
                                          headers={"WWW-Authenticate": "Bearer"})
    token_data = verify_access_token(token, credentials_exception)

    user_id = token_data.id
    cache_key = f"user:{user_id}"

    cached_user = await factory.cache.get(cache_key)
    if cached_user:
        return json.loads(cached_user)

    user_repo = UserRepository(factory.db)
    user = await user_repo.get_by_id(user_id)

    if not user:
        raise credentials_exception  # If user is not found, raise exception

    user_json = UserOut.model_validate(user).model_dump()
    await factory.cache.set(cache_key, json.dumps(user_json), ex=CACHE_TTL)

    return user
