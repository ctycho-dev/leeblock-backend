# from abc import ABC, abstractmethod
# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
# from sqlalchemy.ext.asyncio import async_sessionmaker
# from app.core.config import settings


# class IDatabaseConnection(ABC):
#     @abstractmethod
#     async def get_session(self) -> AsyncSession:
#         pass


# class AsyncSQLAlchemyConnection(IDatabaseConnection):
#     """
#     Async SQLAlchemy implementation.
#     """

#     def __init__(self, database_url: str):
#         self._engine = create_async_engine(
#             database_url,
#             pool_size=10,
#             max_overflow=20,
#             pool_pre_ping=True,
#             pool_recycle=1800,
#             echo=False,
#             future=True
#         )
#         self._Session = async_sessionmaker(
#             bind=self._engine,
#             class_=AsyncSession,
#             autocommit=False,
#             autoflush=False
#         )

#     async def get_session(self) -> AsyncSession:
#         return self._Session()


# DATABASE_URL = (
#     f"postgresql+asyncpg://{settings.db_username}:{settings.db_password}"
#     f"@{settings.db_hostname}:{settings.db_port}/{settings.db_name}"
# )

# db_connection = AsyncSQLAlchemyConnection(DATABASE_URL)


# async def get_db():
#     """Get database session."""
#     async with db_connection.get_session() as db:
#         try:
#             yield db
#         finally:
#             await db.close()