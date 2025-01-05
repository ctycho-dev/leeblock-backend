"""Products schemas."""
from typing import Optional
from pydantic import BaseModel, ConfigDict


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
