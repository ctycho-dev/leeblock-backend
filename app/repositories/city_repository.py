from typing import List
from sqlalchemy.engine import Result
from sqlalchemy.future import select
from app.models.city import City
from app.repositories.base import BaseRepository


class CityRepository(BaseRepository[City]):
    """
    Repository class for managing Request entities.
    """

    def __init__(self, session):
        super().__init__(session, City)

    async def get_by_sequence(self) -> List[City]:
        """
        Retrieve cities by sequence.

        Returns:
            List[City]: A list of cities.
        """
        result: Result = await self.session.execute(
            select(self.model).order_by(self.model.sequence)
        )

        return result.scalars().all()

