"""
Todo api routes module.
"""

from fastapi import APIRouter, status, HTTPException
from src import crud
from src.api.dependencies import UserIdDep
from src.schemas.todo import TodoAdd, TodoRead


router = APIRouter(prefix="/todo", tags=["Todo"])


@router.get("")
async def get_todo_list() -> list[TodoRead]:
    todo_list = crud.get_todo_list()
    return todo_list


@router.get("/{todo_id}")
async def get_todo_by_id(todo_id: int, user_id: UserIdDep) -> TodoRead:
    try:
        todo = crud.get_todo(user_id, todo_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The todo with this id does not exist in the system.",
        )
    return todo


@router.post("", status_code=status.HTTP_201_CREATED)
async def add_todo(user_id: UserIdDep, data: TodoAdd) -> dict[str, str]:
    crud.add_todo(user_id, data)
    return {"status": "OK"}


@router.delete(
    "/todo/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_todo(user_id: UserIdDep, todo_id: int):
    crud.delete_todo(user_id, todo_id)


@router.put("/todo/{todo_id}")
async def update_todo(
    todo_id: int,
    user_id: UserIdDep,
    data: TodoAdd,
):
    try:
        crud.update_todo(user_id, todo_id, data)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The todo with this id does not exist in the system.",
        )
    return {"status": "OK"}
