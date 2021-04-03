import json

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    username: EmailStr

    def to_json(self):
        return json.loads(json.dumps(self, default=lambda x: x.__dict__))


class SimpleUser(UserBase):
    password: str = Field(regex=r'(?=.*\d)(?=.*[a-zA-Z])(?=.*[@#$%&])[\da-zA-Z@#$%&]{8,}')

