from sqlalchemy import Date, Enum, String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domains._base import BaseModel


class Message(BaseModel):
    __tablename__ = "messages"

    telegram_id: Mapped[int] = mapped_column(Integer, unique=True)
    from_user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE")
    )
    sender_chat_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("chats.id", ondelete="CASCADE")
    )
    text: Mapped[str | None] = mapped_column(String)
