from fastapi import APIRouter, HTTPException, status

from sqlalchemy import select, insert

from src.api.dependencies import SessionDep, UserIdDep
from src.models.user import UserOrm
from src.schemas.user import UserRead, UserAddRequest, UserAdd


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("")
async def get_me(user_id: UserIdDep, session: SessionDep) -> UserRead:
    query = select(UserOrm).where(UserOrm.id == user_id)
    result = await session.execute(query)
    user = result.scalars().one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with the provided id not found in the system.",
        )
    return UserRead.model_validate(user, from_attributes=True)


@router.post("")
async def register_user(
    user_data: UserAddRequest,
    session: SessionDep,
):
    password_hash = user_data.password  # TODO: hash the password
    _user_data = UserAdd(username=user_data.username, password_hash=password_hash)
    statement = insert(UserOrm).values(_user_data.model_dump())
    await session.execute(statement)
    await session.commit()
    return {"status": "OK"}
