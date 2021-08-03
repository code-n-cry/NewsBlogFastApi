import pydantic
from pydantic.class_validators import validator
from pydantic.fields import Field
from typing import Optional
from datetime import datetime


class UserBase(pydantic.BaseModel):
    id: int
    nickname: str
    email: pydantic.EmailStr
    is_superuser: bool = False


class UserCreate(pydantic.BaseModel):
    nickname: str
    email: pydantic.EmailStr
    password: str


class User(pydantic.BaseModel):
    nickname: str
    email: pydantic.EmailStr
    is_active: bool


class UserUpdate(pydantic.BaseModel):
    nickname: str
    password: str


class TokenBase(pydantic.BaseModel):
    access_token: str
    token_type: str


class TokenData(pydantic.BaseModel):
    username: Optional[str] = None


class UserPublic(User):
    access_token: Optional[TokenBase]
        