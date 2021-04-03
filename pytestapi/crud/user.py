from pytestapi.enum import UserStatus
from pytestapi.models.user import User as UserModel
from pytestapi.forms.user import SimpleUser
from pytestapi.database import db


def authenticate_user(user):
    with db.not_commit():
        db_user = db().query(UserModel).filter(UserModel.username == user.username).first()
    return db_user if (db_user and UserModel.verify_password(user.password, db_user.hashed_password)) else None


def get_user_by_id(user_id: int):
    with db.not_commit():
        return db().query(UserModel).filter(UserModel.id == user_id).first()


def get_user_by_username(username: str):
    with db.not_commit():
        return db().query(UserModel).filter(UserModel.username == username).first()


def get_users(offset: int = 0, limit: int = 100):
    with db.not_commit():
        return db().query(UserModel).offset(offset).limit(limit).all()


def get_users_count():
    with db.not_commit():
        return db().query(UserModel).count()


def create_user(user: SimpleUser):
    db_user = UserModel()
    db_user.set_attrs(user.to_json())
    with db.auto_commit(db_user):
        db().add(db_user)
    return db_user


def set_user_status(db_user: UserModel, status: UserStatus):
    with db.auto_commit():
        db_user.status = status


def delete_user(user: UserModel):
    with db.auto_commit():
        db().query(UserModel).filter(UserModel.id == user.id).update({'trash': True})
    return user
