from abc import ABC, abstractmethod
from typing import TypeVar

from sqlalchemy import delete, select, update, func
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.domains._base.exceptions import (CreateFailedException,
                                          CreateIntegrityException,
                                          CRUDException, DeleteFailedException,
                                          NotFoundException,
                                          UpdateFailedException)
from app.domains._base.model import BaseModel

T = TypeVar("T", bound=BaseModel)


class BaseCRUDInterface[T](ABC):
    @abstractmethod
    async def create(self, obj: T) -> T: ...

    @abstractmethod
    async def get_by_id(self, id: int) -> T | None: ...

    @abstractmethod
    async def update(self, id: int, data: dict) -> T: ...

    @abstractmethod
    async def delete(self, id: int) -> None: ...

    @abstractmethod
    def create_sync(self, obj: T) -> T: ...

    @abstractmethod
    def get_by_id_sync(self, id: int) -> T | None: ...

    @abstractmethod
    def update_sync(self, id: int, data: dict) -> T: ...

    @abstractmethod
    def delete_sync(self, id: int) -> None: ...

    @abstractmethod
    def get_all(self) -> list[T]: ...


class CRUDRepository(BaseCRUDInterface[T]):
    model: type[T]

    def __init__(self, session: AsyncSession | Session):
        self.session = session

    # -------------------- #
    #   Async CRUD         #
    # -------------------- #

    async def create(self, obj: T) -> T:
        try:
            self.session.add(obj)
            await self.session.commit()
            await self.session.refresh(obj)
            return obj
        except IntegrityError as e:
            await self.session.rollback()
            print(f"[DEBUG] SQLAlchemy error: {type(e).__name__} — {e}")
            raise CreateIntegrityException(
                f"Integrity error on create {self.model.__name__}"
            ) from e
        except SQLAlchemyError as e:
            await self.session.rollback()
            print(f"[DEBUG] SQLAlchemy error: {type(e).__name__} — {e}")
            raise CreateFailedException(
                f"Failed to create {self.model.__name__}"
            ) from e

    async def get_by_id(self, id: int) -> T | None:
        try:
            stmt = select(self.model).where(self.model.id == id)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            raise CRUDException(
                f"Failed to get {self.model.__name__} by id={id}"
            ) from e

    async def get_by_telegram_id(self, telegram_id: int) -> T | None:
        """
        Get model instance by telegram_id.
        Requires that self.model defines a `telegram_id` column.
        """
        try:
            stmt = select(self.model).where(self.model.telegram_id == telegram_id)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            raise CRUDException(
                f"Failed to get {self.model.__name__} by id={id}"
            ) from e
        except AttributeError as ae:
            print(
                f"[DEBUG]: {self.model.__name__} does not have attribute 'telegram_id'"
            )
            raise AttributeError(
                f"{self.model.__name__} does not have attribute 'telegram_id'"
            ) from ae

    async def update(self, id: int, data: dict) -> T:
        try:
            stmt = (
                update(self.model)
                .where(self.model.id == id)
                .values(**data)
                .returning(self.model)
            )
            result = await self.session.execute(stmt)
            updated = result.scalar_one_or_none()
            if updated is None:
                raise NotFoundException(f"{self.model.__name__} id={id} not found")
            await self.session.commit()
            return updated
        except NotFoundException:
            raise
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise UpdateFailedException(
                f"Failed to update {self.model.__name__} id={id}"
            ) from e

    async def delete(self, id: int) -> None:
        try:
            stmt = delete(self.model).where(self.model.id == id)
            result = await self.session.execute(stmt)
            if result.rowcount == 0:
                raise NotFoundException(f"{self.model.__name__} id={id} not found")
            await self.session.commit()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DeleteFailedException(
                f"Failed to delete {self.model.__name__} id={id}"
            ) from e

    # -------------------- #
    #   Sync CRUD          #
    # -------------------- #

    def create_sync(self, obj: T) -> T:
        try:
            self.session.add(obj)
            self.session.commit()
            self.session.refresh(obj)
            return obj
        except IntegrityError as e:
            self.session.rollback()
            print(f"[DEBUG] SQLAlchemy error: {type(e).__name__} — {e}")
            raise CreateIntegrityException(
                f"Integrity error on create {self.model.__name__}"
            ) from e
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"[DEBUG] SQLAlchemy error: {type(e).__name__} — {e}")
            raise CreateFailedException(
                f"Failed to create {self.model.__name__}"
            ) from e

    def get_by_id_sync(self, id: int) -> T | None:
        try:
            stmt = select(self.model).where(self.model.id == id)
            result = self.session.execute(stmt)
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            raise CRUDException(
                f"Failed to get {self.model.__name__} by id={id}"
            ) from e

    def get_by_telegram_id_sync(self, telegram_id: int) -> T | None:
        """
        Get model instance by telegram_id.
        Requires that self.model defines a `telegram_id` column.
        """
        try:
            stmt = select(self.model).where(self.model.telegram_id == telegram_id)
            result = self.session.execute(stmt)
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            raise CRUDException(
                f"Failed to get {self.model.__name__} by id={id}"
            ) from e
        except AttributeError as ae:
            print(
                f"[DEBUG]: {self.model.__name__} does not have attribute 'telegram_id'"
            )
            raise AttributeError(
                f"{self.model.__name__} does not have attribute 'telegram_id'"
            ) from ae

    def update_sync(self, id: int, data: dict) -> T:
        try:
            stmt = (
                update(self.model)
                .where(self.model.id == id)
                .values(**data)
                .returning(self.model)
            )
            result = self.session.execute(stmt)
            updated = result.scalar_one_or_none()
            if updated is None:
                raise NotFoundException(f"{self.model.__name__} id={id} not found")
            self.session.commit()
            return updated
        except NotFoundException:
            raise
        except SQLAlchemyError as e:
            self.session.rollback()
            raise UpdateFailedException(
                f"Failed to update {self.model.__name__} id={id}"
            ) from e

    def delete_sync(self, id: int) -> None:
        try:
            stmt = delete(self.model).where(self.model.id == id)
            result = self.session.execute(stmt)
            if result.rowcount == 0:
                raise NotFoundException(f"{self.model.__name__} id={id} not found")
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise DeleteFailedException(
                f"Failed to delete {self.model.__name__} id={id}"
            ) from e

    def get_all(self) -> list[T]:
        try:
            stmt = select(self.model)
            result = self.session.execute(stmt)
            return list(result.scalars())
        except SQLAlchemyError as e:
            raise CRUDException(
                f"Failed to get {self.model.__name__} by id={id}"
            ) from e

    def get_all_count(self) -> int:
        try:
            stmt = select(func.count()).select_from(self.model)
            result = self.session.execute(stmt)
            count = result.scalar_one()
            return count
        except SQLAlchemyError as e:
            raise CRUDException(
                f"Failed to count {self.model.__name__} records"
            ) from e

