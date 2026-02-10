from fastapi import FastAPI, status
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
def find_todo(todo_id) -> list[TodoRead]:
    """Метод для нахождения todo по индексу"""
    global todo_list
    for item in todo_list:
        if item["id"] == todo_id:
            return TodoRead.model_validate(item)
        return None


@app.get("/todo")
async def get_todo_list() -> list[TodoRead]:
    return [TodoRead.model_validate(item) for item in todo_list]

@app.get("/todo/{todo_id}")
async def get_todo_for_id(todo_id: int) -> list[TodoRead]:
    return [find_todo(todo_id)]

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

@app.patch("/todo")
async def patching_todo(data: TodoRead) -> None:
    ...


@app.put("/todo")
async def update_todo(data: TodoRead) -> None:
    ...



if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
