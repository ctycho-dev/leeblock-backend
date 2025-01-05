"""Products schemas."""
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


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
