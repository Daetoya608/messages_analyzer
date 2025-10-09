from pyrogram.types import Chat as TgChat

from app.core.db.connection import get_session
from app.domains._base.exceptions import (
    CreateFailedException,
    CreateIntegrityException,
    CRUDException,
    DeleteFailedException,
    NotFoundException,
    UpdateFailedException,
)
from app.domains.chats.model import Chat
from app.domains.chats.repository import ChatRepository
from app.domains.chats.schemas import ChatRead, ChatCreate, ChatUpdate

class ChatService:
    def __init__(self, chat_repo: ChatRepository):
        self.chat_repo = chat_repo

    async def create_chat(self, chat_create: ChatCreate) -> ChatRead | None:
        try:
            new_chat = Chat(**chat_create.model_dump())
            result = await self.chat_repo.create(new_chat)
            return ChatRead.model_validate(result)
        except (CreateIntegrityException, CreateFailedException) as e:
            print(f"Произошла ошибка: {e}. Проверьте ввод.")
            return None


    async def create_chat_by_obj(self, chat: TgChat):
        try:
            chat_create = ChatCreate(
                telegram_id=chat.id,
                title=chat.title
            )
            result = await self.create_chat(chat_create)
            return result
        except Exception as e:
            print(f"Произошла ошибка: {e}. Проверьте ввод.")
            return None


    async def get_chat_by_id(self, chat_id: int) -> ChatRead | None:
        try:
            chat = await self.chat_repo.get_by_id(chat_id)
            return ChatRead.model_validate(chat)
        except (NotFoundException, CRUDException) as e:
            print(f"Произошла ошибка: {e}. Проверьте ввод.")
            return None


    async def get_all_messages(self, chat_id: int) -> list[ChatRead]:
        try:
            messages = await self.chat_repo.get_all_messages(chat_id)
            return list(map(ChatRead.model_validate, messages))
        except (NotFoundException, CRUDException) as e:
            print(f"Произошла ошибка: {e}. Проверьте ввод.")
            return []


async def get_chat_service():
    session = await get_session()
    chat_repo = ChatRepository(session)
    return ChatService(chat_repo)