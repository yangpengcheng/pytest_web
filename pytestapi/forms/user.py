import json

from pydantic import BaseModel


class UserBase(BaseModel):
    email: str

    def to_json(self):
        return json.loads(json.dumps(self, default=lambda x: x.__dict__))


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    nickname = str
    trash: bool = False

    class Config:
        orm_mode = True
