from typing import List
from sqlalchemy.future import select
from app.models.product import Product
from app.repositories.base import BaseRepository
from sqlalchemy.engine import Result


class ProductRepository(BaseRepository[Product]):
    """
    Repository class for managing Request entities.
    """

    def __init__(self, session):
        super().__init__(session, Product)

    async def get_all_published(self) -> List[Product]:
        """
        Retrieve requests by their status.

        Args:
            status (str): The status of the requests to retrieve.

        Returns:
            List[Requests]: A list of requests matching the status.
        """
        result: Result = await self.session.execute(
            select(self.model).filter_by(published=1).order_by(self.model.sequence)
        )
        return result.scalars().all()
    
    async def get_to_display(self) -> List[Product]:
        """
        Retrieve requests by their status.

        Args:
            status (str): The status of the requests to retrieve.

        Returns:
            List[Requests]: A list of requests matching the status.
        """
        result: Result = await self.session.execute(
            select(self.model).filter_by(display_on_main=1)
        )
        return result.scalars().all()
