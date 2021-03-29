from datetime import timedelta, datetime

from jose import jwt

from pytestapi.config import SECRET_KEY, ALGORITHM


class Token:
    __slots__ = ('sub', 'expire_minutes')

    def __init__(self, sub, expire_minutes):
        self.sub = sub
        self.expire_minutes = expire_minutes

    def generate_token(self):
        expires_delta = timedelta(minutes=self.expire_minutes)
        to_encode = {"sub": self.sub}.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
