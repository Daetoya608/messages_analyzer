from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.ext.asyncio import AsyncSession


from app.domains._base.repository import CRUDRepository
from app.domains.messages.model import Message
from app.domains._base.exceptions import (CreateFailedException,
                                          CreateIntegrityException,
                                          CRUDException, DeleteFailedException,
                                          NotFoundException,
                                          UpdateFailedException)


class MessageRepository(CRUDRepository[Message]):
    def __init__(self, session: Session | AsyncSession):
        super().__init__(session)
        self.model = Message

    def get_last_messages(self, chat_id: int, message_count: int) -> list[Message]:
        try:
            stmt = (
                select(Message)
                .where(Message.sender_chat_id == chat_id)
                .order_by(Message.date.desc())
                .limit(message_count)
                .options(joinedload(Message.user))  # сразу подгрузить автора
            )
            result = self.session.execute(stmt)
            messages = list(result.scalars().all())
            return list(reversed(messages))  # вернуть в хронологическом порядке (старое -> новое)
        except SQLAlchemyError as e:
            raise CRUDException(
                f"Failed to get last {message_count} messages for chat_id={chat_id}"
            ) from e
