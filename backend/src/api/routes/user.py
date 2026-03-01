from fastapi import APIRouter, HTTPException, status

from sqlalchemy import select, insert
from sqlalchemy.exc import IntegrityError

from src.api.deps import SessionDep, UserIdDep
from src.models.user import UserOrm
from src.schemas.user import UserRead, UserAddRequest, UserAdd
from src.security import hash_password, verify_password


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("")
async def get_me(user_id: UserIdDep, session: SessionDep) -> UserRead:
    query = select(UserOrm).where(UserOrm.id == user_id)
    result = await session.execute(query)
    user = result.scalars().one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return UserRead.model_validate(user, from_attributes=True)


@router.post("/login")
async def login(
    form_data: UserAddRequest,
    session: SessionDep,
):
    query = select(UserOrm).filter_by(username=form_data.username)
    result = await session.execute(query)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    if not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
        )
    # Create access token
    return {"status": "Okey Dokey"}


@router.post("")
async def create_user(
    user_data: UserAddRequest,
    session: SessionDep,
):
    hashed_password = hash_password(user_data.password)
    _user_data = UserAdd(
        username=user_data.username,
        password_hash=hashed_password,
    )
    statement = insert(UserOrm).values(_user_data.model_dump())
    try:
        await session.execute(statement)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with the provided username already exists",
        )
    await session.commit()
    return {"status": "OK"}
