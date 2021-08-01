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
    email: str
    password: str


class UserUpdate(pydantic.BaseModel):
    nickname: str
    password: str


class TokenBase(pydantic.BaseModel):
    token: pydantic.UUID4 = Field(..., alias="acces_token")
    expires: datetime
    token_type: Optional[str] = "bearer"

    class Config:
        allow_population_by_field_name = True

    @validator("token")
    def hexify_token(cls, value):
        return value.hex


class User(UserBase):
    token: TokenBase = {}
