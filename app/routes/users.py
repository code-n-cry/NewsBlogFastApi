from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.utils.dependecies import get_current_user
import app.schemas.users as users
import app.utils.users as users_utils

router = APIRouter()


@router.post("/signup", response_model=users.User)
async def create_user(user: users.UserCreate):
    print(user.dict())
    if await users_utils.get_user_by_email(user.email):
        raise HTTPException(status_code=400, detail="Email already exist!")
    return await users_utils.create_user(user=user)


@router.post("/auth", response_model=users.TokenBase)
async def auth(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await users_utils.get_user_by_email(email=form_data.username)
    if not user or not users_utils.validate_password(password=form_data.password, hashed_password=user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    return await users_utils.create_users_token(user_id=user["id"])


@router.get("/users/me", response_model=users.UserBase)
async def read_users_me(current_user: users.User = Depends(get_current_user)):
    return current_user
