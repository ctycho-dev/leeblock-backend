"""Products schemas."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, field_serializer


class RequestsResponse(BaseModel):
    """Schema for product response details."""

    id: int
    amount: int
    bug: str
    city: str
    zip: str
    address: str
    first_name: str
    last_name: str
    phone: str
    email: str
    status: str
    payment_id: Optional[str]
    token: Optional[str]
    created_at: datetime

    @field_serializer('created_at')
    def serialize_dt(self, created_at: datetime):
        """Convert `created_at` to ISO 8601 string during the validation process."""
        return created_at.isoformat()

    model_config = ConfigDict(from_attributes=True)
