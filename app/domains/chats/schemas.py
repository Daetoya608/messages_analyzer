from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field
from pyrogram.enums import ChatType


class ChatBase(BaseModel):
    telegram_id: Annotated[int, Field(...)]
    chat_type: Annotated[ChatType, Field(...)]
    title: Annotated[str | None, Field(default=None)]
    first_name: Annotated[str | None, Field(default=None)]
    last_name: Annotated[str | None, Field(default=None)]


class ChatCreate(ChatBase):
    pass


class ChatRead(ChatBase):
    id: Annotated[int, Field(...)]
    created_at: Annotated[datetime, Field(...)]
    updated_at: Annotated[datetime, Field(...)]

    model_config = ConfigDict(from_attributes=True)


class ChatUpdate(BaseModel):
    title: Annotated[str | None, Field(None)]
    first_name: Annotated[str | None, Field(None)]
    last_name: Annotated[str | None, Field(None)]
