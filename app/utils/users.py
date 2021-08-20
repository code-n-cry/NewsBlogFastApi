from app.config import database
from app.data.user import table_of_users
from app.schemas import users as user_schema
from passlib.context import CryptContext
from sqlalchemy import select


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)


def validate_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)


async def get_user_by_email(email):
    query = select([table_of_users.c.nickname, table_of_users.c.email, table_of_users.c.is_active]).select_from(table_of_users).where(table_of_users.c.email == email)
    user = await database.fetch_one(query)
    if user:
        user = dict(user)
        user = user_schema.UserPublic(**dict(user))
    return user


async def authenticate_user(username, password):
    user = await get_user_by_email(username)
    if user:
        query = select([table_of_users.c.hashed_password]).where(table_of_users.c.email == user.email)
        hashed_password = await database.fetch_one(query)
        if validate_password(password, dict(hashed_password)["hashed_password"]):
            return user
    return False


async def create_user(user: user_schema.UserCreate):
    hashed_password = hash_password(user.password)
    query = table_of_users.insert().values(
        email=user.email, nickname=user.nickname, hashed_password=f"{hashed_password}", is_superuser=False
    )
    await database.execute(query)
    return user_schema.UserPublic(email=user.email, nickname=user.nickname)
