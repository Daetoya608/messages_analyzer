from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.db import Base
from app.core.config import get_settings


class SessionManager:
    """
    A class that implements the necessary functionality for working with the database:
    issuing sessions, storing and updating connection settings.
    """

    def __init__(self) -> None:
        self.refresh()

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super().__new__(cls)
        return cls.instance  # noqa

    def get_session_maker(self) -> sessionmaker:
        return sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)

    def refresh(self) -> None:
        self.engine = create_async_engine(
            get_settings().database_uri, echo=True, future=True
        )


async def init_models() -> None:
    """
    Создаёт все таблицы в базе данных, если их ещё нет.
    """
    from app.domains import User, Chat, Message
    engine = SessionManager().engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Таблицы успешно созданы (или уже существовали).")


async def get_session() -> AsyncSession:
    session_maker = SessionManager().get_session_maker()
    session = session_maker()
    return session


__all__ = [
    "get_session",
    "SessionManager",
]
