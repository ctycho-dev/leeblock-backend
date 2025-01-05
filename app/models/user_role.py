"""Users realted models."""
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import Integer, String
from app.db.database import Base


class UserRole(Base):
    __tablename__ = 'user_role'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
