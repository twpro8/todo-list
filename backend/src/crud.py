from src.data import todo_list
from src.schemas.todo import TodoRead, TodoAdd


def get_todo_list() -> list[TodoRead]:
    return [TodoRead.model_validate(item) for item in todo_list]


def get_todo(user_id: int, todo_id: int) -> TodoRead:
    todo = get_todo_or_none(user_id, todo_id)
    if not todo:
        raise ValueError
    return TodoRead.model_validate(todo)


def get_todo_or_none(user_id: int, todo_id: int) -> dict | None:
    todo = next(
        (
            todo
            for todo in todo_list
            if todo["id"] == todo_id and todo["user_id"] == user_id
        ),
        None,
    )
    return todo


def add_todo(user_id: int, data: TodoAdd) -> None:
    todo_list.append(
        {
            "id": todo_list[-1]["id"] + 1,
            "user_id": user_id,
            "name": data.name,
        }
    )


def update_todo(user_id: int, todo_id: int, data: TodoAdd):
    todo = get_todo_or_none(user_id, todo_id)
    if todo is None:
        raise ValueError
    todo["name"] = data.name


def delete_todo(user_id: int, todo_id: int) -> None:
    global todo_list
    todo_list = [
        item
        for item in todo_list
        if item["id"] != todo_id and item["user_id"] == user_id
    ]
