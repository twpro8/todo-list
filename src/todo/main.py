from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
import uvicorn


app = FastAPI()


# Database tables
class User:
    id: int
    username: str
    password_hash: str


class Todo:
    id: int
    user_id: int # fk
    name: str


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


@app.get("/todo")
async def get_todo_list() -> list[TodoRead]:
    return [TodoRead.model_validate(item) for item in todo_list]


@app.get("/todo/{todo_id}")
async def get_todo(todo_id: int) -> TodoRead:
    user_id = 1
    todo = [item for item in todo_list if item["user_id"] == user_id and item["id"] == todo_id] 
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return TodoRead.model_validate(todo[0])


@app.post("/todo", status_code=status.HTTP_201_CREATED)
async def add_todo(data: TodoAdd) -> list[TodoRead]:
    todo_list.append({
        "id": 3,
        **data.model_dump()
    })
    return [TodoRead.model_validate(item) for item in todo_list]


@app.delete(
    "/todo/{todo_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_todo(todo_id: int):
    global todo_list
    todo_list = [
        item for item in todo_list 
        if item["id"] != todo_id 
        and item["user_id"] == 1
    ]


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
