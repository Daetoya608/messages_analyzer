from datetime import date, datetime
from typing import Annotated, Self

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class MessageBase(BaseModel):
    telegram_id: Annotated[int, Field(...)]
    from_user_id: Annotated[int, Field(...)]
    sender_chat_id: Annotated[int, Field(...)]
    text: Annotated[str | None, Field(default=None)]


class MessageCreate(MessageBase):
    pass


class MessageRead(MessageBase):
    id: Annotated[int, Field(...)]
    created_at: Annotated[datetime, Field(...)]
    updated_at: Annotated[datetime, Field(...)]

    model_config = ConfigDict(from_attributes=True)


class MessageUpdate(BaseModel):
    text: Annotated[str | None, Field(default=None)]
