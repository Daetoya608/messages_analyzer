
from pyrogram.types import Chat as TgChat

from app.domains._base.exceptions import (CreateFailedException,
                                          CreateIntegrityException,
                                          CRUDException, NotFoundException)
from app.domains.chats.model import Chat
from app.domains.chats.repository import ChatRepository
from app.domains.chats.schemas import ChatCreate, ChatRead


class ChatService:
    def __init__(self, chat_repo: ChatRepository):
        self.chat_repo = chat_repo

    async def create_chat(self, chat_create: ChatCreate) -> ChatRead | None:
        try:
            find_chat = await self.get_chat_by_telegram_id(chat_create.telegram_id)
            if find_chat:
                return find_chat
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
                chat_type=chat.type,
                title=chat.title,
                first_name=chat.first_name,
                last_name=chat.last_name,
            )
            result = await self.create_chat(chat_create)
            return result
        except Exception as e:
            print(f"Произошла ошибка: {e}. Проверьте ввод.")
            return None

    async def get_chat_by_id(self, chat_id: int) -> ChatRead | None:
        try:
            chat = await self.chat_repo.get_by_id(chat_id)
            if chat:
                return ChatRead.model_validate(chat)
            return None
        except (NotFoundException, CRUDException) as e:
            print(f"Произошла ошибка: {e}. Проверьте ввод.")
            return None

    async def get_chat_by_telegram_id(self, telegram_id) -> ChatRead | None:
        try:
            chat = await self.chat_repo.get_by_telegram_id(telegram_id)
            if chat:
                return ChatRead.model_validate(chat)
            return None
        except (NotFoundException, CRUDException, AttributeError) as e:
            print(f"Произошла ошибка: {e}. Проверьте ввод.")
            return None

    def create_chat_sync(self, chat_create: ChatCreate) -> ChatRead | None:
        try:
            new_chat = Chat(**chat_create.model_dump())
            result = self.chat_repo.create_sync(new_chat)
            return ChatRead.model_validate(result)
        except (CreateIntegrityException, CreateFailedException) as e:
            print(f"Произошла ошибка: {e}. Проверьте ввод.")
            return None

    def create_chat_by_obj_sync(self, chat: TgChat):
        try:
            chat_create = ChatCreate(telegram_id=chat.id, title=chat.title)
            result = self.create_chat_sync(chat_create)
            return result
        except Exception as e:
            print(f"Произошла ошибка: {e}. Проверьте ввод.")
            return None

    def get_chat_by_id_sync(self, chat_id: int) -> ChatRead | None:
        try:
            chat = self.chat_repo.get_by_id_sync(chat_id)
            if chat:
                return ChatRead.model_validate(chat)
            return None
        except (NotFoundException, CRUDException) as e:
            print(f"Произошла ошибка: {e}. Проверьте ввод.")
            return None

    def get_all_chats(self) -> list[ChatRead]:
        try:
            chats = self.chat_repo.get_all()
            return list(map(ChatRead.model_validate, chats))
        except (NotFoundException, CRUDException) as e:
            print(f"Произошла ошибка: {e}. Проверьте ввод.")
            return []


def get_chat_service(session):
    chat_repo = ChatRepository(session)
    chat_service = ChatService(chat_repo)
    return chat_service
