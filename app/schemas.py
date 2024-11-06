from datetime import datetime
from dataclasses import dataclass
from typing import Optional, Annotated
from pydantic import BaseModel, EmailStr


@dataclass
class ValueRange:
    """range values"""
    lo: int
    hi: int


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime 

    class Config:
        from_attributes = True


class CityOut(BaseModel):
    code: int
    name: str


class EmailCallbackIn(BaseModel):

    name: str
    phone: str
