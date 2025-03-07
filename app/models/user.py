from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy import Integer, String, ForeignKey, Boolean
from app.db.database import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    phone: Mapped[str] = mapped_column(String)
    admin: Mapped[int] = mapped_column(Integer, default=0)
    is_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    updated_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP,
        server_default=text('now()'),
        onupdate=text('now()')
    )
    created_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text('now()')
    )

    # One-to-many relationship with PromoCode
    promo_codes: Mapped[list["PromoCode"]] = relationship("PromoCode", back_populates="user")


class PromoCode(Base):
    """
    Represents a promo code created by a KOL.
    """

    __tablename__ = "promo_codes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    code: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    discount_type: Mapped[str] = mapped_column(String, nullable=False)
    discount_value: Mapped[int] = mapped_column(Integer, nullable=False)
    used_count: Mapped[int] = mapped_column(Integer, default=0)
    valid_until: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, nullable=False)
    created_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text('now()')
    )

    user: Mapped["User"] = relationship("User", back_populates="promo_codes")
    requests: Mapped[list["Request"]] = relationship("Request", back_populates="promo_code")