from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, Enum, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domains._base import BaseModel


class Chat(BaseModel):
    __tablename__ = "chats"

    telegram_id: Mapped[int] = mapped_column(Integer, unique=True)
    title: Mapped[str] = mapped_column(String)
