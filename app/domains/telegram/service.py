from pyrogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.domains.chats.service import ChatService, get_chat_service
from app.domains.messages.service import MessageService, get_message_service
from app.domains.users.service import UserService, get_user_service


class TelegramService:
    def __init__(
        self,
        message_service: MessageService,
        chat_service: ChatService,
        user_service: UserService,
    ):
        self.message_service = message_service
        self.chat_service = chat_service
        self.user_service = user_service

    async def process_new_message(self, message: Message):
        user = await self.user_service.create_user_by_obj(message.from_user)
        chat = await self.chat_service.create_chat_by_obj(message.chat)
        await self.message_service.create_message_by_obj(message, user.id, chat.id)


def get_telegram_service(session: AsyncSession | Session) -> TelegramService:
    chat_service = get_chat_service(session)
    user_service = get_user_service(session)
    message_service = get_message_service(session)
    return TelegramService(message_service, chat_service, user_service)
