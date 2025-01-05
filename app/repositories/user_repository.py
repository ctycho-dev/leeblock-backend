from typing import Optional
from sqlalchemy.future import select
from app.models.user import User
from app.schemas.users import UserCreate
from app.repositories.base import BaseRepository
from app.utils import oauth2


class UserRepository(BaseRepository[User]):
    """
    Repository class for managing User entities.
    """
    def __init__(self, session):
        super().__init__(session, User)

    async def create_user(self, entity: UserCreate) -> User:
        """
        Create a new user.

        Args:
            entity (UserCreate): The user data to create the new user.

        Returns:
            User: The created user entity.
        """
        # Check if the user already exists
        existing_user = await self.session.execute(select(User).filter_by(username=entity.username))
        existing_user = existing_user.scalars().first()
        if existing_user:
            raise ValueError(f"User with username {entity.username} already exists.")

        # Hash the password before storing
        hashed_password = oauth2.hash_pwd(entity.password)
        entity.password = hashed_password

        new_user = User(**entity.model_dump())
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)

        return new_user

    async def get_by_username(self, username: str) -> Optional[User]:
        """
        Retrieve a user by its username.

        Args:
            username (str): The username of the user.

        Returns:
            Optional[User]: The user entity if found, otherwise None.
        """
        result = await self.session.execute(select(User).filter_by(username=username))
        user = result.scalars().first()

        return user
