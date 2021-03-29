import json

from fastapi import HTTPException as _HTTPException


class Base:
    def deserialization(self) -> dict:
        from sqlalchemy.orm import class_mapper
        columns = [c.key for c in class_mapper(self.__class__).columns]
        return {c: getattr(self, c) for c in columns}

    def serialization(self) -> str:
        return json.dumps(self.deserialization(), default=lambda x: x.__dict__)


class HTTPException:
    def __init__(self, result, reverse=False):
        self.result = result
        self.reverse = reverse

    def __call__(self, status_code, detail, headers=None):
        if headers is None:
            headers = {}
        if (True if self.result else False) ^ (not self.reverse):
            raise _HTTPException(status_code=status_code, detail=detail, headers=headers)
