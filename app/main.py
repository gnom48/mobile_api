from fastapi import FastAPI
from .api import router_users, router_notes, router_tasks, router_teams
from contextlib import asynccontextmanager
from .database import create_tables, drop_tables

# & c:/Users/Egorc/Desktop/mobile_api/venv/Scripts/Activate.ps1
# uvicorn main:app --reload --host --port 8000

@asynccontextmanager
async def lifespan(app: FastAPI):
    await drop_tables()
    print("Удалено")
    await create_tables()
    print("Создано")
    yield
    print("Выключение")


app = FastAPI(lifespan=lifespan)
app.include_router(router_teams)
app.include_router(router_notes)
app.include_router(router_tasks)
app.include_router(router_users)
