"""Requests realted models."""
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String
from app.db.database import Base


class City(Base):
    """Cities table."""
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    code: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    sequence: Mapped[int] = mapped_column(Integer, nullable=False)
