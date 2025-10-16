from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


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
