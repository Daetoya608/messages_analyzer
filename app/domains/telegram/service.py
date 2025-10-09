from pyrogram.types import Message
from app.domains.messages.service import MessageService, get_message_service
from app.domains.chats.service import ChatService, get_chat_service
from app.domains.users.service import UserService, get_user_service
from app.core.db.connection import get_session

class TelegramService:
    def __init__(self, message_service: MessageService, chat_service: ChatService, user_service: UserService):
        self.message_service = message_service
        self.chat_service = chat_service
        self.user_service = user_service


    async def process_new_message(self, message: Message):
        await self.user_service.create_user_by_obj(message.from_user)
        await self.chat_service.create_chat_by_obj(message.chat)
        await self.message_service.create_message_by_obj(message)


async def get_telegram_service():
    chat_service = await get_chat_service()
    user_service = await get_user_service()
    message_service = await get_message_service()
    return TelegramService(message_service, chat_service, user_service)
