from fastapi import APIRouter

from src.api.routes import user
from src.api.routes import todo

api_router = APIRouter()
api_router.include_router(user.router)
api_router.include_router(todo.router)
