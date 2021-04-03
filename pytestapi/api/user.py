from fastapi import Depends, APIRouter
from fastapi import status

from pytestapi.authenticate import get_current_active_user, User

from pytestapi.crud import user as user_crud
from pytestapi.util.cal import cal_offset
from pytestapi.view_models.base import HTTPException
from pytestapi.view_models.user import UserView, UserCollection


router = APIRouter(prefix='/users', tags=['user'])


@router.get('/', description='获取用户列表')
async def get_users(page: int = 0, per_page: int = 100):
    db_users = user_crud.get_users(offset=cal_offset(page,per_page), limit=per_page)
    total = user_crud.get_users_count()
    users = UserCollection()
    users.fill(db_users, total)
    return users


@router.get('/me', description='获取当前用户')
async def get_user_me(current_user: User = Depends(get_current_active_user)):
    return UserView(current_user)


@router.get('/{user_id}', description='根据id查找用户')
async def query_user(user_id: int):
    db_user = user_crud.get_user_by_id(user_id=user_id)
    HTTPException(db_user)(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")
    return UserView(db_user)
