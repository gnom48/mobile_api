from pydantic import BaseModel
from enum import Enum
from datetime import datetime
from typing import Optional


class StatisticPeriods(str, Enum):
    DAY_STATISTICS_PERIOD = "day"
    WEEK_STATISTICS_PERIOD = "week"
    MONTH_STATISTICS_PERIOD = "month"


class UserTypes(str, Enum):
    COMMERCIAL = "Риелтер коммерческой недвижимости"
    PRIVATE = "Риелтер частной недвижимости"


class WorkTasksTypes(str, Enum):
    FLYERS = "Рассклейка"
    CALLS = "Обзвон"
    SHOW = "Показ объекта"
    MEET = "Встреча по объекту"
    DEAL = "Сделка"
    DEPOSIT = "Получение задатка"
    SEARCH = "Поиск объектов"
    ANALYTICS = "Аналитика рынка"


class User(BaseModel):
    id: int
    login: str
    password: str
    type: UserTypes
    photo: str

    name: str
    gender: Optional[str]
    birthday: Optional[int]
    phone: Optional[str]


class Note(BaseModel):
    id: int
    title: str
    desc: Optional[str]
    date_time: int
    user_id: int
    notification_id: int


class Task(BaseModel):
    id: int
    work_type: WorkTasksTypes
    date_time: int
    desc: Optional[str]
    duration_seconds: int
    user_id: int


class Team(BaseModel):
    id: int
    name: str
    created_date_time: datetime
    

class UserStatuses(str, Enum):
    OWNER = "Владелец"
    USER = "Участник"


class UserTeam(BaseModel):
    team_id: int
    user_id: int
    role: UserStatuses
    
    
class Statistics(BaseModel):
    user_id: int
    data: int

class StatisticsOrm(BaseModel):
    user_id: int
    flyers: int
    calls: int
    shows: int
    meets: int
    deals: int
    deposits: int
    searches: int
    analytics: int
    others: int