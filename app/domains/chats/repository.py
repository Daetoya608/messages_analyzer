from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains._base.repository import CRUDRepository
from app.domains.chats.model import Chat


class ChatRepository(CRUDRepository[Chat]):
    def __init__(self, session: Session | AsyncSession):
        super().__init__(session)
        self.model = Chat
