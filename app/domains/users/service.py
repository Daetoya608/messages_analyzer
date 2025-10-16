from pyrogram.types import User as TgUser
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.domains._base.exceptions import (CreateFailedException,
                                          CreateIntegrityException,
                                          CRUDException, NotFoundException)
from app.domains.users.model import User
from app.domains.users.repository import UserRepository
from app.domains.users.schemas import UserCreate, UserRead


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def create_user(self, user_create: UserCreate) -> UserRead | None:
        try:
            find_user = await self.get_chat_by_telegram_id(user_create.telegram_id)
            if find_user is not None:
                return find_user
            new_user = User(**user_create.model_dump())
            result = await self.user_repo.create(new_user)
            return UserRead.model_validate(result)
        except (CreateIntegrityException, CreateFailedException) as e:
            print(f"Произошла ошибка: {e}. Проверьте ввод.")
            return None

    async def create_user_by_obj(self, user: TgUser) -> UserRead | None:
        try:
            user_create = UserCreate(
                telegram_id=user.id,
                first_name=user.first_name,
                last_name=user.last_name,
                username=user.username,
            )
            print(user_create.model_dump())
            result = await self.create_user(user_create)
            return result
        except Exception as e:
            print(f"Произошла ошибка: {e}. Проверьте ввод.")
            return None

    async def get_user_by_id(self, user_id: int) -> UserRead | None:
        try:
            user = await self.user_repo.get_by_id(user_id)
            if user:
                return UserRead.model_validate(user)
            return None
        except (NotFoundException, CRUDException) as e:
            print(f"Произошла ошибка: {e}. Проверьте ввод.")
            return None

    async def get_chat_by_telegram_id(self, telegram_id) -> UserRead | None:
        try:
            chat = await self.user_repo.get_by_telegram_id(telegram_id)
            if chat:
                return UserRead.model_validate(chat)
            return None
        except (NotFoundException, CRUDException, AttributeError) as e:
            print(f"Произошла ошибка: {e}. Проверьте ввод.")
            return None


def get_user_service(session: AsyncSession | Session) -> UserService:
    user_repo = UserRepository(session)
    return UserService(user_repo)
