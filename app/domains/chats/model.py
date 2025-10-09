from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, Enum, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domains._base import BaseModel


class Chat(BaseModel):
    __tablename__ = "chats"

    telegram_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=True)

    messages: Mapped[list["Message"]] = relationship(
        "Message",
        back_populates="chat",
        cascade="all, delete-orphan"
    )
