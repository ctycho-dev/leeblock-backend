from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
# from app.repositories.user_repository import UserRepository
# from app.repositories.request_repository import RequestRepository


class DependencyFactory:
    def __init__(self, db: AsyncSession, cache: Redis):
        self._db = db
        self._cache = cache

    @property
    def db(self) -> AsyncSession:
        """Get the database session."""
        return self._db

    @property
    def cache(self) -> Redis:
        """Get the Redis client."""
        return self._cache

    # def get_user_repository(self) -> UserRepository:
    #     """Create and return a UserRepository instance."""
    #     return UserRepository(db=self.db, redis_client=self.redis)

    # def get_request_repository(self) -> RequestRepository:
    #     """Create and return a RequestRepository instance."""
    #     return RequestRepository(db=self.db, redis_client=self.redis)
