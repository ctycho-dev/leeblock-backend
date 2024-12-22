from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, TEXT
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base


class User(Base):
    """users table"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))


class Cities(Base):
    """users table"""
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True, nullable=False)
    code = Column(Integer, nullable=False, unique=True)
    name = Column(String, nullable=False)
    sequence = Column(Integer, nullable=False)


class Products(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    product_id = Column(String(100), nullable=False, unique=True)
    product_type = Column(String(100))
    description = Column(String(500), nullable=False)
    image = Column(String(500))
    images = Column(String)
    catalog_img = Column(String(500))
    catalog_hover_img = Column(String(500))
    price = Column(Integer, nullable=False)
    supply = Column(Integer, nullable=False, default=0)
    waiting = Column(Integer, nullable=False, default=0)
    sequence = Column(Integer, nullable=False, default=100)
    published = Column(Integer, nullable=False, default=0)
    display_on_main = Column(Integer, nullable=False, default=0)
    weight = Column(Integer, nullable=False, default=0)
    height = Column(Integer, nullable=False, default=0)
    length = Column(Integer, nullable=False, default=0)
    width = Column(Integer, nullable=False, default=0)
    color = Column(String(100))


class Requests(Base):
    __tablename__ = 'requests'

    id = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(Integer, nullable=False)
    bug = Column(String, nullable=False)
    city = Column(String(100), nullable=False)
    zip = Column(String(20))
    address = Column(String(1000), nullable=False)
    first_name = Column(String(255))
    last_name = Column(String(255))
    phone = Column(String(255))
    email = Column(String(255), nullable=False)
    status = Column(String(20), nullable=False, default='NEW')
    payment_id = Column(String(255))
    token = Column(String(255))
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
