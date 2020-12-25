from sqlalchemy import Column, ForeignKey, String, Integer, Boolean
from sqlalchemy.orm import relationship 
from sqlalchemy.types import DateTime
from config import Base 
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key = True,
        index =  True
    )

    firstname = Column(
        String(200),
        nullable = False
    )

    lastname = Column(
        String(200),
        nullable = False
    )

    email = Column(
        String,
        nullable = False
    )

    active = Column(
        Boolean,
        default = False
    )

    password = Column(
        String,
        nullable = False
    )

    created_at = Column(
        DateTime,
        default = datetime.now()
    )

    books = relationship(
        "BookStore",
        back_populates = "user"
    )

class BookStore(Base):

    __tablename__ = "bookstore"

    id = Column(
        Integer,
        primary_key = True,
        index = True
    )

    title = Column(
        String(300),
        nullable = False
    )

    description = Column(
        String(300),
        nullable = False
    )

    category = Column(
        String(300),
        nullable = False
    )

    author = Column(
        String(300),
        nullable = False
    )

    price = Column(
        Integer,
        nullable = False
    )

    quantity = Column(
        Integer,
        nullable = True
    )

    published_year = Column(
        Integer,
        nullable = True
    )

    bestseller = Column(
        Boolean,
        default = False
    )

    created_at = Column(
        DateTime,
        default = datetime.now()
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    user = relationship(
        "User",
        back_populates = "books"
    )

