from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime


def _dump_with_alias(self: BaseModel, **kwargs) -> dict:
    kwargs.setdefault("by_alias", True)
    return super(type(self), self).model_dump(**kwargs)  # type: ignore


class _Base(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)


class CategorySchema(_Base):
    id: Optional[int] = None
    name: Optional[str] = None


class TagSchema(_Base):
    id: Optional[int] = None
    name: Optional[str] = None


class PetSchema(_Base):
    id: Optional[int] = None
    category: Optional[CategorySchema] = None
    name: str
    photo_urls: List[str] = Field(..., alias="photoUrls")
    tags: Optional[List[TagSchema]] = None
    status: Optional[str] = None


class PetFormUpdate(_Base):
    name: Optional[str] = None
    status: Optional[str] = None


class OrderSchema(_Base):
    id: Optional[int] = None
    pet_id: Optional[int] = Field(None, alias="petId")
    quantity: Optional[int] = None
    ship_date: Optional[datetime] = Field(None, alias="shipDate")
    status: Optional[str] = None
    complete: Optional[bool] = False


class UserSchema(_Base):
    id: Optional[int] = None
    username: Optional[str] = None
    first_name: Optional[str] = Field(None, alias="firstName")
    last_name: Optional[str] = Field(None, alias="lastName")
    email: Optional[str] = None
    password: Optional[str] = None
    phone: Optional[str] = None
    user_status: Optional[int] = Field(None, alias="userStatus")


class ApiResponse(_Base):
    code: Optional[int] = None
    type: Optional[str] = None
    message: Optional[str] = None
