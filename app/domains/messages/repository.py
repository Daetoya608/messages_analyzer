from sqlalchemy.ext.asyncio import AsyncSession

from app.domains._base.repository import CRUDException, CRUDRepository
from app.domains.messages.model import Message


class ChatRepository(CRUDRepository[Message]):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.model = Message
