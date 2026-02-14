"""
Database module.
"""

from pathlib import Path
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

engine = create_async_engine(f"sqlite+aiosqlite:///{DATA_DIR / 'app.db'}")
sessionmaker = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with sessionmaker() as session:
        yield session
