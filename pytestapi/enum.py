from enum import Enum, unique


@unique
class UserStatus(Enum):
    ONLINE = 0
    OFFLINE = 1
    LOCKED = 2


@unique
class Trigger(Enum):
    DATE = 'date'
    INTERVAL = 'interval'
    CRON = 'cron'


@unique
class RunStatus(Enum):
    RUNNING = 0
    PAUSED = 1
    STOPED = 2
