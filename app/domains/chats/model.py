
from pyrogram.enums import ChatType
from sqlalchemy import Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domains._base import BaseModel


class Chat(BaseModel):
    __tablename__ = "chats"

    telegram_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    chat_type: Mapped[ChatType] = mapped_column(
        Enum(ChatType, name="chat_type", native_enum=False),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(String, nullable=True)
    first_name: Mapped[str] = mapped_column(String, nullable=True)
    last_name: Mapped[str] = mapped_column(String, nullable=True)

    messages = relationship(
        "Message", back_populates="chat", cascade="all, delete-orphan"
    )
