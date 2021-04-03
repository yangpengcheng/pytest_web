from fastapi import APIRouter, status, Depends
from fastapi.responses import Response
from fastapi.security import OAuth2PasswordRequestForm

from pytestapi.authenticate import get_current_active_user, get_logged_user
from pytestapi.cache import cache_dic
from pytestapi.config import ACCESS_TOKEN_EXPIRE_MINUTES
from pytestapi.enum import UserStatus
from pytestapi.forms.user import SimpleUser
from pytestapi.crud import user as user_crud
from pytestapi.models.user import User
from pytestapi.view_models.base import HTTPException
from pytestapi.models.token import Token as TokenModel
from pytestapi.view_models.token import Token as TokenView

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/login', description='用户登录')
async def login(user: OAuth2PasswordRequestForm = Depends()):
    db_user = user_crud.authenticate_user(user)
    HTTPException(db_user)(status_code=status.HTTP_401_UNAUTHORIZED, detail='用户名或密码错误',
                           headers={'www-authenticate': 'Bearer'})
    HTTPException(db_user.status == UserStatus.LOCKED, reverse=True)(
        status_code=status.HTTP_401_UNAUTHORIZED, detail='用户已被锁定')
    token_temp = TokenModel(sub=user.username, expire_minutes=1).generate_token()
    HTTPException(db_user.status == UserStatus.ONLINE, reverse=True)(
        status_code=status.HTTP_307_TEMPORARY_REDIRECT, detail='用户已登录，重定向到清除token请求页',
        headers={'Location': f'https://0.0.0.0:5000/auth/{user.username}/reset',
                 'token': token_temp})
    token_model = TokenModel(sub=user.username, expire_minutes=ACCESS_TOKEN_EXPIRE_MINUTES).generate_token()
    user_crud.set_user_status(db_user, UserStatus.ONLINE)
    cache_dic[db_user.username] = token_model
    return TokenView(token_model)


@router.delete('/{username}/reset', description="清除登录状态")
async def reset_token(current_user: User = Depends(get_current_active_user)):
    db_user = user_crud.get_user_by_username(current_user.username)
    HTTPException(db_user)(status_code=status.HTTP_404_NOT_FOUND, detail='用户不存在')
    cache_dic['username'] = None
    user_crud.set_user_status(db_user, UserStatus.OFFLINE)
    return Response(status_code=status.HTTP_200_OK)


@router.post('/logout', description="退出登录")
def logout(current_user: User = Depends(get_logged_user)):
    HTTPException(current_user)(status_code=status.HTTP_409_CONFLICT, detail='用户无需退出')
    cache_dic['username'] = None
    db_user = user_crud.get_user_by_username(current_user.username)
    user_crud.set_user_status(db_user, UserStatus.OFFLINE)
    return Response(status_code=status.HTTP_200_OK)


@router.put('/register', description="用户注册")
async def register(user: SimpleUser):
    db_user = await user_crud.get_user_by_username(username=user.username)
    HTTPException(db_user, reverse=True)(status_code=status.HTTP_409_CONFLICT, detail="邮箱已经被注册")
    return Response(status_code=status.HTTP_201_CREATED)
