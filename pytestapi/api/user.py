from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from pytestapi.api import router
from pytestapi.authenticate import get_current_active_user, User
from pytestapi.config import ACCESS_TOKEN_EXPIRE_MINUTES
from pytestapi.forms.user import UserCreate
from pytestapi.models.token import Token as TokenModel
from pytestapi.crud import user as user_crud
from pytestapi.view_models.base import HTTPException
from pytestapi.view_models.token import Token as TokenView
from pytestapi.view_models.user import UserView, UserCollection


@router.post("/user/registered", tags=["用户注册"])
async def user_registered(user: UserCreate):
    db_user = user_crud.get_user_by_email(email=user.email)
    HTTPException(db_user, reverse=True)(status_code=status.HTTP_400_BAD_REQUEST, detail="邮箱已经被注册")
    return UserView(user_crud.create_user(user=user))


@router.post("/user/login", tags=["用户登录"])
async def login(user: OAuth2PasswordRequestForm = Depends()):
    db_user = user_crud.authenticate_user(user)
    HTTPException(db_user)(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误",
                           headers={"www-authenticate": "Bearer"})
    token_model = TokenModel(sub=user.username, expire_minutes=ACCESS_TOKEN_EXPIRE_MINUTES).generate_token()
    return TokenView(token_model)


@router.get("/users", tags=["获取用户列表"])
async def get_users(offset: int = 0, limit: int = 100):
    db_users = user_crud.get_users(offset=offset, limit=limit)
    total = user_crud.get_user_count()
    users = UserCollection()
    users.fill(db_users, total)
    return users


@router.get("/users/me", tags=["获取当前用户"])
async def get_user_me(current_user: User = Depends(get_current_active_user)):
    return UserView(current_user)


@router.get("/users/{user_id}", tags=["根据id查找用户"])
async def query_user(user_id: int):
    db_user = user_crud.get_user_by_id(user_id=user_id)
    HTTPException(db_user)(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")
    return UserView(db_user)
