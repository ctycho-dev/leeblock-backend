"""Requests realted models."""
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from app.db.database import Base


class Request(Base):
    __tablename__ = 'requests'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    bug: Mapped[str] = mapped_column(String, nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    zip: Mapped[str | None] = mapped_column(String(20))
    address: Mapped[str] = mapped_column(String(1000), nullable=False)
    first_name: Mapped[str | None] = mapped_column(String(255))
    last_name: Mapped[str | None] = mapped_column(String(255))
    phone: Mapped[str | None] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default='NEW')
    payment_id: Mapped[str | None] = mapped_column(String(255))
    token: Mapped[str | None] = mapped_column(String(255))
    promo_code_id: Mapped[int | None] = mapped_column(Integer, ForeignKey('promo_codes.id'), nullable=True)
    created_at: Mapped[str] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')
    )

    # Relationship to PromoCode
    promo_code: Mapped["PromoCode"] = relationship("PromoCode", back_populates="requests")