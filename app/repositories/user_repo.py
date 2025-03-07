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

    async def get_all_non_admin_users(self) -> list[User]:
        """
        Retrieve all users where admin is 0.

        Returns:
            List[T]: A list of all non-admin users.
        """
        query = select(self.model).where(self.model.admin == 0)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def create_user(self, entity: UserCreate) -> User:
        """
        Create a new user.

        Args:
            entity (UserCreate): The user data to create the new user.

        Returns:
            User: The created user entity.
        """
        existing_user = await self.session.execute(select(User).filter_by(email=entity.email))
        existing_user = existing_user.scalars().first()
        if existing_user:
            raise ValueError(f"User with username {entity.email} already exists.")

        # Hash the password before storing
        hashed_password = oauth2.hash_pwd(entity.password)
        entity.password = hashed_password

        new_user = User(**entity.model_dump())
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)

        return new_user

    async def verify_user(self, email):
        """
        """
        result = await self.session.execute(select(User).where(User.email == email))
        db_kol = result.scalars().first()
        if not db_kol:
            raise ValueError("User not found")

        db_kol.is_verified = True
        await self.session.commit()
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """
        Retrieve a user by its email.

        Args:
            email (str): The email of the user.

        Returns:
            Optional[User]: The user entity if found, otherwise None.
        """
        result = await self.session.execute(select(User).filter_by(email=email))
        user = result.scalars().first()

        return user
