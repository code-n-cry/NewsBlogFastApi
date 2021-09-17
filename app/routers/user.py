from datetime import timedelta
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy import select
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES
import app.schemas.users as users
from pydantic import BaseModel
from app.config import SECRET_KEY, database
from fastapi_jwt_auth import AuthJWT
import app.utils.users as users_utils
from app.data.user import table_of_users

router = APIRouter()


class Settings(BaseModel):
    authjwt_secret_key: str = SECRET_KEY
    # Configure application to store and get JWT from cookies
    authjwt_token_location: set = {"cookies"}
    authjwt_cookie_secure: bool = False
    authjwt_cookie_csrf_protect: bool = False
    #authjwt_cookie_samesite: str = 'lax'


@AuthJWT.load_config
def get_config():
    return Settings()


@router.post("/signup", response_model=users.UserPublic)
async def create_user(user: users.UserCreate):
    if len(user.password) < 5 or not user.password.isascii():
        raise HTTPException(status_code=400, detail="Incorrect password!")
    if await users_utils.get_user_by_email(user.email):
        raise HTTPException(status_code=400, detail="Email already exists!")
    return await users_utils.create_user(user=user)


@router.put('/users/me')
async def edit_user(user: users.UserUpdate, authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    current_user_email = authorize.get_jwt_subject()
    hashed_password = await database.fetch_one(select([table_of_users.c.hashed_password]).select_from(table_of_users).where(table_of_users.c.email == current_user_email))
    print(users_utils.hash_password(user.password), dict(hashed_password), user.password)
    if users_utils.validate_password(user.password, dict(hashed_password)['hashed_password']):
        await users_utils.edit_user_nickname(user.nickname, current_user_email)
        return {'msg': 'Succesfully changed nickname'}
    else:
        raise HTTPException(status_code=401, detail="Incorrect password")


@router.post("/auth")
async def auth(user: users.UserLogin, authorize: AuthJWT = Depends()):
    user = await users_utils.authenticate_user(user.email, user.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = authorize.create_access_token(
        subject=user.email, expires_time=access_token_expires)
    refresh_token = authorize.create_refresh_token(subject=user.email)
    authorize.set_access_cookies(access_token)
    authorize.set_refresh_cookies(refresh_token)
    return {"msg": "Succesfully login"}


@router.post('/refresh')
def refresh(authorize: AuthJWT = Depends()):
    authorize.jwt_refresh_token_required()
    current_user = authorize.get_jwt_subject()
    new_access_token = authorize.create_access_token(subject=current_user)
    authorize.set_access_cookies(new_access_token)
    return {"msg": "The token has been refresh"}


@router.delete("/logout")
async def logout(authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    authorize.unset_jwt_cookies()
    return {"msg": "Succesfully logout"}


@router.get("/users/me")
async def read_users_me(authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    current_user_email = authorize.get_jwt_subject()
    return await users_utils.get_user_by_email(current_user_email)
