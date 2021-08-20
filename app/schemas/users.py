from pydantic.errors import SetError
import pydantic
from typing import Optional


class UserBase(pydantic.BaseModel):
    id: int
    nickname: str
    email: pydantic.EmailStr
    is_superuser: bool = False


class UserCreate(pydantic.BaseModel):
    nickname: str
    email: pydantic.EmailStr
    password: str


class UserPublic(pydantic.BaseModel):
    nickname: str
    email: pydantic.EmailStr
    is_active: bool = True  


class UserUpdate(pydantic.BaseModel):
    nickname: str
    password: str


class TokenBase(pydantic.BaseModel):
    access_token: str
    token_type: str


class TokenData(pydantic.BaseModel):
    username: Optional[str] = None


class UserLogin(pydantic.BaseModel):
    email: str
    password: str
