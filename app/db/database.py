from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.core.config import settings


DATABASE_URL = (
    f"postgresql+asyncpg://{settings.db_username}:{settings.db_password}"
    f"@{settings.db_hostname}:{settings.db_port}/{settings.db_name}"
)

Base = declarative_base()

# Create Async Engine
engine = create_async_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=1800,
    echo=False,
    future=True
)

# Create Async Session Factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False
)


async def get_db():
    """Get database session."""
    db = AsyncSessionLocal()
    try:
        yield db
    # except Exception:
    #     db.rollback()
    finally:
        await db.close()
