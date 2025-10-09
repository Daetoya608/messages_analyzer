from datetime import date, datetime
from typing import Annotated, Self
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    telegram_id: Annotated[int, Field(...)]
    first_name: Annotated[str | None, Field(default=None)]
    last_name: Annotated[str | None, Field(default=None)]
    username: Annotated[str, Field(...)]


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: Annotated[int, Field(...)]
    created_at: Annotated[datetime, Field(...)]
    updated_at: Annotated[datetime, Field(...)]

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    first_name: Annotated[str | None, Field(default=None)]
    last_name: Annotated[str | None, Field(default=None)]
    username: Annotated[str | None, Field(default=None)]
