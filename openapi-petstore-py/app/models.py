from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, Table, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.database import Base

pet_tags = Table(
    "pet_tags",
    Base.metadata,
    Column("pet_id", Integer, ForeignKey("pets.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
)


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    pets = relationship("Pet", back_populates="category")


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    pets = relationship("Pet", secondary=pet_tags, back_populates="tags")


class Pet(Base):
    __tablename__ = "pets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    photo_urls = Column(String, nullable=False)
    status = Column(String, nullable=False)

    category = relationship("Category", back_populates="pets")
    tags = relationship("Tag", secondary=pet_tags, back_populates="pets")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    pet_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    ship_date = Column(DateTime, nullable=True)
    status = Column(String, nullable=False)
    complete = Column(Boolean, default=False)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    password = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    user_status = Column(Integer, default=0)
