from sqlalchemy import Date, Enum, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domains._base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(Integer, unique=True)
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    username: Mapped[str] = mapped_column(String)
