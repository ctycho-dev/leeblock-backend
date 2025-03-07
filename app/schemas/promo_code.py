from datetime import datetime, timedelta
import enum
from pydantic import BaseModel


class DiscountType(str, enum.Enum):
    """
    Enum for discount types.
    """

    PERCENTAGE = "percentage"
    FIXED_AMOUNT = "fixed_amount"


class PromoCodeCreate(BaseModel):
    """
    Pydantic model for promo code creation request.
    """
    user_id: int
    code: str
    discount_type: DiscountType
    discount_value: int
    max_uses: int = 1000
    valid_until: datetime = datetime.now() + timedelta(days=365)
    # discount_type: DiscountType = DiscountType.PERCENTAGE
    # discount_value: int = 5
    # max_uses: int = 100
    # valid_until: datetime = datetime.now() + timedelta(days=365)
