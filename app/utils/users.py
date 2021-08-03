from datetime import datetime, timedelta
from sqlalchemy import and_
from app.config import database
from app.data.user import table_of_users, table_of_tokens
from app.schemas import users as user_schema
from app.config import SECRET_KEY, ALGORITHM
from typing import Optional
from passlib.context import CryptContext
from sqlalchemy import select
from jose import jwt


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)


def validate_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)


async def get_user_by_email(email):
    query = select([table_of_users.c.nickname, table_of_users.c.email, table_of_users.c.hashed_password, table_of_users.c.is_active]).select_from(table_of_users).where(table_of_users.c.email == email)
    user = await database.fetch_one(query)
    if user:
        user = dict(user)
        user = user_schema.User(**dict(user))
    return user
 

async def get_user_by_token(token):
    query = table_of_tokens.join(table_of_users).select().where(
        and_(
            table_of_tokens.c.token == token,
            table_of_tokens.c.expires > datetime.now()
        )
    )
    return await database.fetch_one(query)


async def authenticate_user(username, password):
    user = await get_user_by_email(username)
    if user:
        query = select([table_of_users.c.hashed_password]).where(table_of_users.c.email == user.email)
        hashed_password = await database.fetch_one(query)
        if validate_password(password, dict(hashed_password)["hashed_password"]):
            return user
    return False


async def create_access_token(data: dict, exipres_delta: Optional[timedelta] = None):
    value_to_encode = data.copy()
    if exipres_delta:
        expire = datetime.utcnow() + exipres_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    value_to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(value_to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt


async def create_user(user: user_schema.UserCreate):
    hashed_password = hash_password(user.password)
    query = table_of_users.insert().values(
        email=user.email, nickname=user.nickname, hashed_password=f"{hashed_password}", is_superuser=False
    )
    await database.execute(query)
    token = await create_access_token({"email": user.email, "nickname": user.nickname})
    token_dict = user_schema.TokenBase(access_token=token, token_type="bearer")
    return user_schema.UserPublic(email=user.email, nickname=user.nickname, is_active=True, access_token=token_dict)
 