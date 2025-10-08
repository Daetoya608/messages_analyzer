from sqlalchemy.ext.asyncio import AsyncSession

from app.domains._base.repository import CRUDException, CRUDRepository
from app.domains.chats.model import Chat


class ChatRepository(CRUDRepository[Chat]):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.model = Chat
