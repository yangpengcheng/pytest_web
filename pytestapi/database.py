from contextlib import contextmanager
from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from pytestapi.config import SQLALCHEMY_DATABASE_URL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, encoding='utf-8', echo=False)
_sessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)
_Base = declarative_base()


class Base(_Base):
    __abstract__ = True
    create_time = Column('create_time', Integer)
    trash = Column('trash', Boolean, default=False)

    def __init__(self):
        self.create_time = int(datetime.now().timestamp())

    def set_attrs(self, attrs):
        for key, value in attrs.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    @property
    def create_datetime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None


class SessionLocal:
    def __init__(self):
        self.session = _sessionLocal()

    def __call__(self):
        return self.session

    @contextmanager
    def auto_commit(self, table_data=None, throw=True):
        try:
            yield
            self().commit()
            if table_data:
                self().flush(table_data)
        except Exception as e:
            self().rollback()
            if throw:
                raise e

    @contextmanager
    def not_commit(self, throw=True):
        try:
            yield
        except Exception as e:
            if throw:
                raise e


db = SessionLocal()
