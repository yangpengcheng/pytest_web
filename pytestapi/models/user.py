from passlib.context import CryptContext
from sqlalchemy import Column, Integer, String

from pytestapi.database import Base
from pytestapi.enum import UserStatus

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    nickname = Column(String, default='默认昵称')
    hashed_password = Column(String)
    _authority = Column("authority", String, default='general')
    _status = Column("status", Integer, default=1)

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    def set_attrs(self, attrs):
        for key, value in attrs.items():
            if hasattr(self, key) and key != 'id' and key != 'password':
                if key != 'password':
                    setattr(self, key, value)
            setattr(self, 'hashed_password', self.get_password_hash(value))

    @property
    def status(self):
        return UserStatus(self._status)

    @status.setter
    def status(self, _status):
        self._status = _status.value

    @property
    def authority(self):
        return self._authority.split(',')

    @authority.setter
    def authority(self, _authority):
        self._authority = ','.join(_authority)
