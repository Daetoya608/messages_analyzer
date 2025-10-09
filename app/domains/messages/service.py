from pyrogram.types import Message as TgMessage

from app.core.db.connection import get_session
from app.domains._base.exceptions import (
    CreateFailedException,
    CreateIntegrityException,
    CRUDException,
    DeleteFailedException,
    NotFoundException,
    UpdateFailedException,
)
from app.domains.messages.model import Message
from app.domains.messages.repository import MessageRepository
from app.domains.messages.schemas import MessageRead, MessageCreate, MessageUpdate


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


    async def create_message_by_obj(self, message: TgMessage) -> MessageRead | None:
        try:
            message_create = MessageCreate(
                telegram_id=message.id,
                from_user_id=message.from_user.id,
                sender_chat_id=message.chat.id,
                text=message.text
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


async def get_message_service():
    session = await get_session()
    message_repo = MessageRepository(session)
    return MessageService(message_repo)
