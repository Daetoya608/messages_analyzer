from pyrogram.types import Message as TgMessage
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.domains._base.exceptions import (CreateFailedException,
                                          CreateIntegrityException,
                                          CRUDException, NotFoundException)
from app.domains.messages.model import Message
from app.domains.messages.repository import MessageRepository
from app.domains.messages.schemas import (MessageCreate, MessageRead, MessageReadFull)


class MessageService:
    def __init__(self, message_repo: MessageRepository):
        self.message_repo = message_repo

    async def create_message(self, message_create: MessageCreate) -> MessageRead | None:
        try:
            new_message = Message(**message_create.model_dump())
            result = await self.message_repo.create(new_message)
            return MessageRead.model_validate(result)
        except (CreateIntegrityException, CreateFailedException) as e:
            print(f"Произошла ошибка: {e}. Проверьте ввод.")
            return None

    async def create_message_by_obj(self, message: TgMessage, from_user_id: int, sender_chat_id: int) -> MessageRead | None:
        try:
            message_create = MessageCreate(
                telegram_id=message.id,
                from_user_id=from_user_id,
                sender_chat_id=sender_chat_id,
                text=message.text,
                date=message.date,
            )
            result = await self.create_message(message_create)
            return result
        except Exception as e:
            print(f"Произошла ошибка: {e}. Проверьте ввод.")
            return None

    async def get_message_by_id(self, message_id: int) -> MessageRead | None:
        try:
            message = await self.message_repo.get_by_id(message_id)
            return MessageRead.model_validate(message)
        except (NotFoundException, CRUDException) as e:
            print(f"Произошла ошибка: {e}. Проверьте ввод.")
            return None


    def get_message_by_id_sync(self, message_id: int) -> MessageRead | None:
        try:
            message = self.message_repo.get_by_id_sync(message_id)
            return MessageRead.model_validate(message)
        except (NotFoundException, CRUDException) as e:
            print(f"Произошла ошибка: {e}. Проверьте ввод.")
            return None

    def get_last_messages(self, chat_id: int, message_count: int):
        try:
            messages = self.message_repo.get_last_messages(chat_id, message_count)
            return list(map(MessageReadFull.model_validate, messages))
        except (NotFoundException, CRUDException) as e:
            print(f"Произошла ошибка: {e}. Проверьте ввод.")
            return None


def get_message_service(session: AsyncSession | Session) -> MessageService:
    message_repo = MessageRepository(session)
    return MessageService(message_repo)
