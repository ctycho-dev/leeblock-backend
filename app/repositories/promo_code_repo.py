from typing import Optional
from sqlalchemy.future import select
from app.models.user import PromoCode
from app.models.user import User
from app.repositories.base import BaseRepository


class PromoCodeRepository(BaseRepository[PromoCode]):
    """
    Repository class for managing KolUser entities.
    """
    def __init__(self, session):
        super().__init__(session, PromoCode)

    async def get_all_with_user(self) -> list[dict]:
        """
        Retrieve all promo codes along with the associated user's email.

        Returns:
            List[dict]: A list of dictionaries containing promo code details and user email.
        """
        # Define the join between promocodes and users tables
        query = (
            select(PromoCode, User.email)
            .join(User, PromoCode.user_id == User.id)
        )

        result = await self.session.execute(query)

        promocodes_with_emails = [
            {
                "id": promo_code.id,
                "code": promo_code.code,
                "discount_type": promo_code.discount_type,
                "discount_value": promo_code.discount_value,
                "valid_until": promo_code.valid_until,
                "used_count": promo_code.used_count,
                "user_email": email,
            }
            for promo_code, email in result
        ]

        return promocodes_with_emails
    
    async def get_by_code(self, code: str) -> Optional[dict]:
        """
        Retrieve a promo code by its code along with the associated user's email.

        Args:
            code (str): The promo code to search for.

        Returns:
            Optional[dict]: A dictionary containing promo code details and user email, or None if not found.
        """
        # Define the join between promocodes and users tables
        query = (
            select(PromoCode, User.email)
            .join(User, PromoCode.user_id == User.id)
            .where(PromoCode.code == code)
        )

        # Execute the query
        result = await self.session.execute(query)

        # Fetch the first result (if any)
        promo_code_with_email = result.first()

        if promo_code_with_email:
            promo_code, email = promo_code_with_email
            return {
                "id": promo_code.id,
                "code": promo_code.code,
                "discount_type": promo_code.discount_type,
                "discount_value": promo_code.discount_value,
                "valid_until": promo_code.valid_until,
                "used_count": promo_code.used_count,
                "user_email": email,  # Include the user's email
            }

        return None  # Return None if no promo code is found

    async def get_by_user_id(self, user_id: int):
        """
        Retrieve a user by its email.

        Args:
            email (str): The email of the user.

        Returns:
            Optional[User]: The user entity if found, otherwise None.
        """
        result = await self.session.execute(select(PromoCode).filter_by(user_id=user_id))
        promo = result.scalars().all()

        return promo
