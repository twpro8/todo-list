"""
Main module.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi.routing import APIRoute
from src.api import todo
from src.api import user
from src.database import Base, engine
from src.models.todo import TodoOrm
from src.models.user import UserOrm

API_V1_STR = "/api/v1"

@asynccontextmanager
async def lifespan(app: FastAPI):
    # create db tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(todo.router, prefix=API_V1_STR)
app.include_router(user.router, prefix=API_V1_STR)
