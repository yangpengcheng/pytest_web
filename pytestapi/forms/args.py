from typing import Optional

from pydantic import BaseModel


class PytestArg(BaseModel):
    r_arg: str
    p_arg: str = ''
    d_arg: str = ''


class JobArg(BaseModel):
    command: str = ''
    id: str
    trigger: str
    announcer: str
    subscriber: str
    year: Optional[str] = None
    month: Optional[str] = None
    day: Optional[str] = None
    week: Optional[str] = None
    day_of_week: Optional[str] = None
    hour: Optional[str] = None
    minute: Optional[str] = None
    second: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    timezone: Optional[str] = None
    jitter: Optional[int] = None
    run_date: Optional[str] = None
    weeks: Optional[int] = None
    days: Optional[int] = None
    hours: Optional[int] = None
    minutes: Optional[int] = None
    seconds: Optional[int] = None

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if k not in ['command', 'id', 'trigger'] and v}


class ID(BaseModel):
    id: str


class Object(BaseModel):
    name: str
    val: dict
