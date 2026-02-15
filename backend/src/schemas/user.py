from pydantic import BaseModel


class UserRead(BaseModel):
    id: int
    username: str


class UserAddRequest(BaseModel):
    username: str
    password: str


class UserAdd(BaseModel):
    username: str
    password_hash: str
