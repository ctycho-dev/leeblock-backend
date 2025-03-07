from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict, field_serializer
from datetime import datetime


class UserCreate(BaseModel):
    """
    Schema for creating a new user.

    Attributes:
        email (EmailStr): The user's email address.
        password (str): The user's password.
    """
    email: EmailStr
    password: str
    first_name: Optional[str]
    last_name: Optional[str]
    phone: Optional[str]


class UserUpdate(BaseModel):
    """
    Schema for user login credentials.

    Attributes:
        email (EmailStr): The user's email address.
        password (str): The user's password.
    """
    first_name: str | None
    last_name: str | None
    phone: str | None


class UserUpdatePassword(BaseModel):
    """
    Schema for user login credentials.

    Attributes:
        email (EmailStr): The user's email address.
        password (str): The user's password.
    """
    password: str


class UserOut(BaseModel):
    """
    Schema for returning user details.

    Attributes:
        id (int): The user's unique identifier.
        email (EmailStr): The user's email address.
        created_at (datetime): The timestamp when the user was created.
    """
    id: int
    email: EmailStr
    first_name: str | None
    last_name: str | None
    phone: str | None
    admin: int
    is_verified: bool
    created_at: datetime

    @field_serializer('created_at')
    def serialize_dt(self, created_at: datetime):
        """Convert `created_at` to ISO 8601 string during the validation process."""
        return created_at.isoformat()

    model_config = ConfigDict(from_attributes=True)


class TokenData(BaseModel):
    """
    Schema for returning user details.

    Attributes:
        id (int): The user's unique identifier.
        email (EmailStr): The user's email address.
        created_at (datetime): The timestamp when the user was created.
    """

    id: Optional[int] = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    """Login response."""

    access_token: str
    token_type: str
