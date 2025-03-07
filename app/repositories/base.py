from typing import Generic, TypeVar, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy import desc

T = TypeVar("T", bound=DeclarativeMeta)


class BaseRepository(Generic[T]):
    """
    Base class for repository implementations.
    Provides default implementations for common operations.
    """

    def __init__(self, session: AsyncSession, model: T):
        """
        Initialize the repository with a database session and model.

        Args:
            session (AsyncSession): Database session for asynchronous operations.
            model (T): SQLAlchemy model class associated with this repository.
        """
        self.session = session
        self.model = model

    async def get_by_id(self, entity_id: int) -> Optional[T]:
        """
        Retrieve an entity by its ID.

        Args:
            entity_id (int): The ID of the entity.

        Returns:
            Optional[T]: The entity if found, otherwise None.
        """
        result = await self.session.execute(select(self.model).filter_by(id=entity_id))
        return result.scalars().first()

    async def get_all(self) -> List[T]:
        """
        Retrieve all entities.

        Returns:
            List[T]: A list of all entities.
        """
        result = await self.session.execute(
            select(self.model).order_by(desc(self.model.created_at))
        )
        return result.scalars().all()
        # result = await self.session.execute(select(self.model))
        # return result.scalars().all()

    async def add(self, entity: T) -> T:
        """
        Add a new entity.

        Args:
            entity (T): The entity to add.

        Returns:
            T: The added entity.
        """
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity

    async def update(self, entity: T) -> T:
        """
        Update an existing entity.

        Args:
            entity (T): The entity to update.

        Returns:
            T: The updated entity.
        """
        await self.session.merge(entity)
        await self.session.commit()
        return entity

    async def delete(self, entity_id: int) -> None:
        """
        Delete an entity by its ID.

        Args:
            entity_id (int): The ID of the entity to delete.
        """
        entity = await self.get_by_id(entity_id)
        if entity:
            await self.session.delete(entity)
            await self.session.commit()



# from abc import ABC, abstractmethod
# from typing import Generic, TypeVar, Optional, List
# from sqlalchemy.ext.asyncio import AsyncSession

# T = TypeVar("T")


# class BaseRepository(ABC, Generic[T]):
#     """
#     Abstract base class for repository implementations.

#     Enforces derived classes to implement specific repository methods.
#     """

#     def __init__(self, session: AsyncSession):
#         """
#         Initialize the repository with a database session.

#         Args:
#             session (AsyncSession): Database session for asynchronous operations.
#         """
#         self.session = session

#     @abstractmethod
#     async def get_by_id(self, entity_id: int) -> Optional[T]:
#         """
#         Retrieve an entity by its ID.

#         Args:
#             entity_id (int): The ID of the entity.

#         Returns:
#             Optional[T]: The entity if found, otherwise None.
#         """

#     @abstractmethod
#     async def get_all(self) -> List[T]:
#         """
#         Retrieve all entities.

#         Returns:
#             List[T]: A list of all entities.
#         """

#     @abstractmethod
#     async def add(self, entity: T) -> T:
#         """
#         Add a new entity.

#         Args:
#             entity (T): The entity to add.

#         Returns:
#             T: The added entity.
#         """

#     @abstractmethod
#     async def update(self, entity: T) -> T:
#         """
#         Update an existing entity.

#         Args:
#             entity (T): The entity to update.

#         Returns:
#             T: The updated entity.
#         """

#     @abstractmethod
#     async def delete(self, entity_id: int) -> None:
#         """
#         Delete an entity by its ID.

#         Args:
#             entity_id (int): The ID of the entity to delete.
#         """
