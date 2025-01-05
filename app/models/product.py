"""Products realted models."""
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import Integer, String
from app.db.database import Base


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    product_id: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    product_type: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    image: Mapped[str] = mapped_column(String(500))
    images: Mapped[str] = mapped_column(String)
    catalog_img: Mapped[str] = mapped_column(String(500))
    catalog_hover_img: Mapped[str] = mapped_column(String(500))
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    supply: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    waiting: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    sequence: Mapped[int] = mapped_column(Integer, nullable=False, default=100)
    published: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    display_on_main: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    weight: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    height: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    length: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    width: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    color: Mapped[str] = mapped_column(String(100))
