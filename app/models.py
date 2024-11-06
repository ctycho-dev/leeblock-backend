from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
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
