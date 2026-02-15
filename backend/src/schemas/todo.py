from pydantic import BaseModel


class TodoAddRequest(BaseModel):
    name: str


class TodoAdd(TodoAddRequest):
    user_id: int


class TodoRead(TodoAdd):
    id: int
