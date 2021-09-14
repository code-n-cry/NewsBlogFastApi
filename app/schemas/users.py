import pydantic
from typing import Optional


class EmailStr(str):  # type: ignore
    pass


class UserBase(pydantic.BaseModel):
    id: int
    nickname: str
    email: EmailStr
    is_superuser: bool = False


class UserCreate(pydantic.BaseModel):
    nickname: str
    email: EmailStr
    password: str


class UserPublic(pydantic.BaseModel):
    nickname: str
    email: EmailStr
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
