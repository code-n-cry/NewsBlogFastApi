import hashlib, random, string
from datetime import datetime, timedelta
from sqlalchemy import and_
from app.config import database
from app.data.user import table_of_users, table_of_tokens
from app.schemas import users as user_schema


def generate_seed(length=12):
    return "".join(random.choice(string.ascii_letters) for _ in range(length))


def hash_password(password: str, seed : str = generate_seed()):
    password = password.encode()
    seed = seed.encode()
    hashed_password = hashlib.pbkdf2_hmac("sha256", password, seed, 100_000)
    return hashed_password.hex()


def validate_password(password: str, hashed_password):
    seed, hash = hashed_password.split("$")
    return hash_password(password.encode(), seed) == hash


async def get_user_by_email(email):
    query = table_of_users.select().where(table_of_users.c.email == email)
    return await database.fetch_one(query)
 

async def get_user_by_token(token):
    query = table_of_tokens.join(table_of_users).select(table_of_users.c.id).where(
        and_(
            table_of_tokens.c.token == str(token),
            table_of_tokens.c.expires > datetime.now()
        )
    )
    return await database.fetch_one(query)


async def create_users_token(user_id):
    query = (
        table_of_tokens.insert().values(expires=datetime.now() + timedelta(hours=1), user_id=user_id)
        .returning(table_of_tokens.c.token, table_of_tokens.c.expires)
    )
    return await database.fetch_one(query)


async def create_user(user: user_schema.UserCreate):
    seed = generate_seed()
    hashed_password = hash_password(user.password, seed)
    query = table_of_users.insert().values(
        email=user.email, nickname=user.nickname, hashed_password=f"{seed}${hashed_password}"
    )
    user_id = await database.execute(query)
    token = await create_users_token(user_id)
    token_dict = {"token": token["token"], "expires": token["expires"]}

    return {**user.dict(), "id": user_id, "is_active": True, "token": token_dict}
