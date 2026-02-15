"""
Main module.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api import todo
from src.api import user
from src.database import Base, engine
from src.models.todo import TodoOrm
from src.models.user import UserOrm


@asynccontextmanager
async def lifespan(app: FastAPI):
    # create db tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(todo.router)
app.include_router(user.router)
