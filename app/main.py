from fastapi import FastAPI
from .api import router_users, router_notes, router_tasks, router_teams
from contextlib import asynccontextmanager
from .repository import Repository
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .database import create_tables, drop_tables
from apscheduler.triggers.cron import CronTrigger


# & c:/Users/Egorc/Desktop/mobile_api/venv/Scripts/Activate.ps1
# uvicorn main:app --reload --host 192.168.0.193 --port 8000

main_scheduler = AsyncIOScheduler(timezone="UTC")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # await drop_tables()
    # print("Удалено")
    # await create_tables()
    # print("Создано")

    main_scheduler.add_job(func=Repository.clear_day_statistics, trigger=CronTrigger(hour=21-3, minute=30))
    main_scheduler.add_job(func=Repository.clear_month_statistics, trigger='cron', day='last', hour=21-3, minute=0)
    main_scheduler.add_job(func=Repository.clear_week_statistics, trigger='cron', day_of_week='mon', hour=21-3, minute=5)

    yield
    print("Выключение")


app = FastAPI(lifespan=lifespan)
app.include_router(router_teams)
app.include_router(router_notes)
app.include_router(router_tasks)
app.include_router(router_users)
