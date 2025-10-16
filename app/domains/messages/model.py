from datetime import datetime

from sqlalchemy import ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domains._base import BaseModel


class Message(BaseModel):
    __tablename__ = "messages"

    telegram_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    from_user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    sender_chat_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("chats.id", ondelete="CASCADE"), nullable=False
    )
    text: Mapped[str | None] = mapped_column(String, nullable=True)
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    user = relationship("User", back_populates="messages")
    chat = relationship("Chat", back_populates="messages")
