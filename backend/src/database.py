session = "some_session"


class Base:
    pass


# Database tables
class User(Base):
    id: int
    username: str
    password_hash: str


class Todo(Base):
    id: int
    user_id: int  # fk
    name: str
