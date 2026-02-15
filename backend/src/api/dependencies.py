from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_session


def get_current_user_id():
    user_id = 1
    return user_id


UserIdDep = Annotated[int, Depends(get_current_user_id)]
SessionDep = Annotated[AsyncSession, Depends(get_session)]
