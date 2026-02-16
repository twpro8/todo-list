"""
Todo api routes module.
"""

from fastapi import APIRouter, status, HTTPException
from sqlalchemy import insert, select, delete, update

from src.api.dependencies import SessionDep, UserIdDep
from src.schemas.todo import TodoAdd, TodoRead, TodoAddRequest
from src.models.todo import TodoOrm


router = APIRouter(prefix="/todos", tags=["Todos"])


@router.get("")
async def get_todo_list(session: SessionDep) -> list[TodoRead]:
    query = select(TodoOrm)
    result = await session.execute(query)
    todo_list = result.scalars().all()
    return [TodoRead.model_validate(todo, from_attributes=True) for todo in todo_list]


@router.get("/{todo_id}")
async def get_todo_by_id(
    todo_id: int, user_id: UserIdDep, session: SessionDep
) -> TodoRead:
    query = select(TodoOrm).where(TodoOrm.id == todo_id, TodoOrm.user_id == user_id)
    result = await session.execute(query)
    todo = result.scalars().one_or_none()
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The todo with this id does not exist in the system.",
        )
    return TodoRead.model_validate(todo, from_attributes=True)


@router.post("", status_code=status.HTTP_201_CREATED)
async def add_todo(
    user_id: UserIdDep,
    session: SessionDep,
    todo_data: TodoAddRequest,
) -> dict[str, str]:
    _todo_data = TodoAdd(user_id=user_id, name=todo_data.name)
    statement = insert(TodoOrm).values(_todo_data.model_dump())
    await session.execute(statement)
    await session.commit()
    return {"status": "OK"}


@router.delete(
    "/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_todo(user_id: UserIdDep, todo_id: int, session: SessionDep):
    statement = delete(TodoOrm).where(TodoOrm.id == todo_id, TodoOrm.user_id == user_id)
    await session.execute(statement)
    await session.commit()


@router.put("/{todo_id}")
async def update_todo(
    todo_id: int,
    user_id: UserIdDep,
    todo_data: TodoAddRequest,
    session: SessionDep,
):
    query = select(TodoOrm).where(TodoOrm.id == todo_id, TodoOrm.user_id == user_id)
    result = await session.execute(query)
    todo = result.scalars().one_or_none()
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The todo with this id does not exist in the system.",
        )

    _todo_data = TodoAdd(user_id=user_id, name=todo_data.name)
    statement = (
        update(TodoOrm)
        .where(TodoOrm.id == todo_id, TodoOrm.user_id == user_id)
        .values(_todo_data.model_dump())
    )
    await session.execute(statement)
    await session.commit()
    return {"status": "OK"}
