from sqlalchemy.ext.asyncio import AsyncSession

from app.domains._base.repository import CRUDException, CRUDRepository
from app.domains.chats.model import Chat
from app.domains.messages.model import Message

class ChatRepository(CRUDRepository[Chat]):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.model = Chat

    async def get_all_messages(self, chat_id: int) -> list[Message]:
        chat = await self.get_by_id(chat_id)
        return chat.messages
