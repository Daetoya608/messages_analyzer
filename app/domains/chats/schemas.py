from datetime import date, datetime
from typing import Annotated, Self
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ChatBase(BaseModel):
    telegram_id: Annotated[int, Field(...)]
    title: Annotated[str | None, Field(default=None)]


class ChatCreate(ChatBase):
    pass


class ChatRead(ChatBase):
    id: Annotated[int, Field(...)]
    created_at: Annotated[datetime, Field(...)]
    updated_at: Annotated[datetime, Field(...)]

    model_config = ConfigDict(from_attributes=True)


class ChatUpdate(BaseModel):
    title: Annotated[str | None, Field(default=None)]
