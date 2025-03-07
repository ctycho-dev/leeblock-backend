"""Payment schemas."""
from typing import List
from pydantic import BaseModel


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
    promo_code_id: int
