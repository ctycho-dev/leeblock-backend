from datetime import datetime
from dataclasses import dataclass
from typing import Optional, List
from pydantic import BaseModel, EmailStr, ConfigDict


@dataclass
class ValueRange:
    """
    Represents a range of integer values with lower and upper bounds.

    Attributes:
        lo (int): The lower bound of the range.
        hi (int): The upper bound of the range.
    """
    lo: int
    hi: int


class UserCreate(BaseModel):
    """
    Schema for creating a new user.

    Attributes:
        email (EmailStr): The user's email address.
        password (str): The user's password.
    """
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    """
    Schema for user login credentials.

    Attributes:
        email (EmailStr): The user's email address.
        password (str): The user's password.
    """
    email: EmailStr
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
    created_at: datetime 

    class Config:
        from_attributes = True


class CityOut(BaseModel):
    """
    Schema for city details.

    Attributes:
        code (int): The unique code of the city.
        name (str): The name of the city.
    """
    code: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class EmailIn(BaseModel):
    """
    Schema for sending email input.

    Attributes:
        subject (str): The subject of the email.
        body (str): The body content of the email.
        msg_type (str): The type of the email message.
    """
    subject: str
    body: str
    msg_type: str


class ProductResponse(BaseModel):
    """
    Schema for product response details.

    Attributes:
        name (str): The name of the product.
        product_id (str): The unique identifier of the product.
        product_type (Optional[str]): The type/category of the product.
        description (str): The description of the product.
        image (Optional[str]): The URL of the product's image.
        catalog_img (Optional[str]): The URL of the catalog image.
        catalog_hover_img (Optional[str]): The URL of the catalog hover image.
        price (int): The price of the product.
        supply (int): The current supply count of the product.
        waiting (int): The number of products in waiting list or queue.
        sequence (int): The display order sequence of the product.
        published (int): Indicates if the product is published (1) or not (0).
        display_on_main (int): Indicates if the product should be displayed on the main page.
        color (Optional[str]): The color of the product.
    """
    name: str
    product_id: str
    product_type: Optional[str] = None
    description: str
    image: Optional[str] = None
    images: Optional[str] = None
    catalog_img: Optional[str] = None
    catalog_hover_img: Optional[str] = None
    price: int
    supply: int = 0
    waiting: int = 0
    sequence: int = 100
    published: int = 0
    display_on_main: int = 0
    color: Optional[str] = None
    weight: int
    height: int
    length: int
    width: int

    model_config = ConfigDict(from_attributes=True)


class CheckoutItems(BaseModel):
    """
    Schema for items in a checkout.

    Attributes:
        Name (str): The name of the item.
        Price (int): The price of a single unit of the item.
        Quantity (int): The quantity of the item purchased.
        Amount (int): The total amount for the item (Price x Quantity).
        Tax (str): The tax details applied to the item.
    """

    Name: str
    Price: int
    Quantity: int
    Amount: int
    Tax: str


class CheckoutData(BaseModel):
    """
    Schema for customer data during checkout.

    Attributes:
        Phone (str): The customer's phone number.
        Email (str): The customer's email address.
    """
    Phone: str
    Email: str


class CheckoutReceipt(BaseModel):
    """
    Schema for the receipt details during checkout.

    Attributes:
        Email (str): The customer's email address.
        Phone (str): The customer's phone number.
        Taxation (str): The taxation details for the receipt.
        Items (List[CheckoutItems]): A list of items in the receipt.
    """
    Email: str
    Phone: str
    Taxation: str
    Items: List[CheckoutItems]


class CheckoutIn(BaseModel):
    """
    Schema for checkout input.

    Attributes:
        Amount (int): The total amount for the checkout.
        DATA (CheckoutData): The customer data.
        Receipt (CheckoutReceipt): The receipt details including items.
        city (str): The city for delivery.
        zip (str): The postal/ZIP code for delivery.
        address (str): The delivery address.
        first_name (str): The customer's first name.
        last_name (str): The customer's last name.
        phone (str): The customer's phone number.
        email (str): The customer's email address.
    """
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


class Packages(BaseModel):
    """
    Schema for product characteristics
    """

    weight: int
    height: int
    length: int
    width: int


class DeliveryIn(BaseModel):
    """
    Schema for getting tarrif of delivery
    """

    city_name: str
    city_code: int
    address: str
    city_zip: str
    packages: List[Packages]
