from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from starlette import status

from pytestapi.config import SECRET_KEY, ALGORITHM
from pytestapi.enum import UserStatus
from pytestapi.models.user import User
from pytestapi.crud import user as user_crud

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="无法验证凭据",
    headers={"www-Authenticate": "bearer"},
)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = user_crud.get_user_by_username(username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.trash:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="无权操作")
    return current_user


async def get_logged_user(current_user: User = Depends(get_current_active_user)):
    if current_user.status != UserStatus.ONLINE:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="用户未登录")
    return current_user
