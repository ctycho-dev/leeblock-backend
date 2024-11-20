from datetime import datetime
from dataclasses import dataclass
from typing import Optional, Annotated, List
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


class EmailIn(BaseModel):

    subject: str
    body: str
    msg_type: str


class ProductsOut(BaseModel):

    name: str
    product_id: str
    product_type: Optional[str] = None
    description: str
    image: Optional[str] = None
    catalog_img: Optional[str] = None
    catalog_hover_img: Optional[str] = None
    price: int
    supply: int = 0
    waiting: int = 0
    sequence: int = 100
    published: int = 0
    display_on_main: int = 0
    color: Optional[str] = None


class CheckoutItems(BaseModel):

    Name: str
    Price: int
    Quantity: int
    Amount: int
    Tax: str


class CheckoutData(BaseModel):

    Phone: str
    Email: str


class CheckoutReceipt(BaseModel):

    Email: str
    Phone: str
    Taxation: str
    Items: List[CheckoutItems]


class CheckoutIn(BaseModel):

    Amount: int
    DATA: CheckoutData
    Receipt: CheckoutReceipt
    city: str
    zip: str
    address: str
    first_name: str
    last_name: str
    phone: str
    email: str
