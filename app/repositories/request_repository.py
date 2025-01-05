from typing import List
from sqlalchemy.future import select
from app.models.request import Request
from app.repositories.base import BaseRepository
from sqlalchemy.engine import Result


class RequestRepository(BaseRepository[Request]):
    """
    Repository class for managing Request entities.
    """

    def __init__(self, session):
        super().__init__(session, Request)

    async def get_by_status(self, status: str) -> List[Request]:
        """
        Retrieve requests by their status.

        Args:
            status (str): The status of the requests to retrieve.

        Returns:
            List[Requests]: A list of requests matching the status.
        """
        result: Result = await self.session.execute(
            select(self.model).filter_by(status=status)
        )
        return result.scalars().all()
