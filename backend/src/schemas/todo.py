from pydantic import BaseModel


class TodoAdd(BaseModel):
    name: str


class TodoRead(BaseModel):
    id: int
    user_id: int
    name: str
