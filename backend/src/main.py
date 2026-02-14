"""
Main module.
"""

from fastapi import FastAPI

from src.api import todo


app = FastAPI()
app.include_router(todo.router)
