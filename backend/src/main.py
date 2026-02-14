from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel


app = FastAPI()


# dto
class TodoAdd(BaseModel):
    name: str


class TodoRead(BaseModel):
    id: int
    user_id: int
    name: str


todo_list = [
    {
        "id": 1,
        "user_id": 1,
        "name": "Cook dinner",
    },
    {
        "id": 2,
        "user_id": 1,
        "name": "Wash the dishes",
    },
]


def get_todo_or_none(todo_id: int, user_id: int) -> dict | None:
    user_id = 1
    todo = next(
        (
            todo
            for todo in todo_list
            if todo["id"] == todo_id and todo["user_id"] == user_id
        ),
        None,
    )
    return todo


@app.get("/todo")
async def get_todo_list() -> list[TodoRead]:
    return [TodoRead.model_validate(item) for item in todo_list]


@app.get("/todo/{todo_id}")
async def get_todo_by_id(todo_id: int) -> TodoRead:
    user_id = 1
    todo = get_todo_or_none(todo_id, user_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The todo with this id does not exist in the system.",
        )
    return TodoRead.model_validate(todo)


@app.post("/todo", status_code=status.HTTP_201_CREATED)
async def add_todo(data: TodoAdd) -> list[TodoRead]:
    user_id = 1
    todo_list.append(
        {
            "id": todo_list[-1]["id"] + 1,
            "user_id": user_id,
            "name": data.name,
        }
    )
    return [TodoRead.model_validate(item) for item in todo_list]


@app.delete(
    "/todo/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_todo(todo_id: int):
    global todo_list
    todo_list = [
        item for item in todo_list if item["id"] != todo_id and item["user_id"] == 1
    ]


@app.put("/todo/{todo_id}")
async def update_todo(
    todo_id: int,
    data: TodoAdd,
):
    user_id = 1
    todo = get_todo_or_none(todo_id, user_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The todo with this id does not exist in the system.",
        )
    todo["name"] = data.name
    return {"status": "OK"}
