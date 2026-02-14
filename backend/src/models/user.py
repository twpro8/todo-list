from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class UserOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(128), unique=True)
    password_hash: Mapped[str]
