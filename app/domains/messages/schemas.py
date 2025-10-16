from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from app.domains.users.schemas import UserRead
from app.domains.chats.schemas import ChatRead
from app.domains.users.utils import get_full_name

class MessageBase(BaseModel):
    telegram_id: Annotated[int, Field(...)]
    from_user_id: Annotated[int, Field(...)]
    sender_chat_id: Annotated[int, Field(...)]
    text: Annotated[str | None, Field(default=None)]
    date: Annotated[datetime, Field(...)]


class MessageCreate(MessageBase):
    pass


class MessageRead(MessageBase):
    id: Annotated[int, Field(...)]
    created_at: Annotated[datetime, Field(...)]
    updated_at: Annotated[datetime, Field(...)]

    model_config = ConfigDict(from_attributes=True)


class MessageUpdate(BaseModel):
    text: Annotated[str | None, Field(default=None)]


class MessageReadFull(MessageRead):
    user: Annotated[UserRead, Field(...)]
    chat: Annotated[ChatRead, Field(...)]

    def __str__(self):
        s = (f"{get_full_name(self.user.first_name, self.user.last_name)} "
             f"({self.user.username}): {self.text}")
        return s
