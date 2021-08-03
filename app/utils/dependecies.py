from app.utils import users as users_utils
from app.schemas.users import TokenData
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from app.config import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")


async def get_current_user(token = Depends(oauth2_scheme)):
    credential_error = HTTPException(
        status_code=401,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        username = payload.get("sub")
        if not username:
            raise credential_error
        token_data = TokenData(username=username)
    except JWTError:
        raise credential_error
    user = await users_utils.get_user_by_email(email=token_data.username) 
    if not user:
        raise credential_error
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user