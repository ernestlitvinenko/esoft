from contextlib import asynccontextmanager
from typing import TypeVar

from sqlalchemy import select, Result, update, delete

from database import Base
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

T = TypeVar('T', bound=Base)


class BaseStorage:

    def __init__(self, session_maker: async_sessionmaker, db_model: type[T]):
        self.DBModel: type[T] = db_model
        self.__session_maker: async_sessionmaker = session_maker

    @asynccontextmanager
    async def get_session(self) -> AsyncSession:
        session = self.__session_maker()
        try:
            yield session
        finally:
            await session.aclose()

    async def get(self, **kwargs) -> T | None:
        where_clauses = [getattr(self.DBModel, key) == value for key, value in kwargs.items()]
        stmt = select(self.DBModel).where(*where_clauses)
        async with self.get_session() as session:
            result: Result = await session.execute(stmt)
            return result.scalars().one_or_none()

    async def get_all(self, **kwargs) -> list[T]:
        where_clauses = [getattr(self.DBModel, key) == value for key, value in kwargs.items()]
        stmt = select(self.DBModel).where(*where_clauses)
        async with self.get_session() as session:
            result: Result = await session.execute(stmt)
            return result.scalars().all()

    async def create(self, **kwargs) -> T:
        db_obj = self.DBModel(**kwargs)
        async with self.get_session() as session:
            session.add(db_obj)
            await session.commit()
            return db_obj

    async def update(self, id: int, **kwargs) -> T:
        stmt = update(self.DBModel).where(self.DBModel.id == id).values(**kwargs).returning(self.DBModel)
        async with self.get_session() as session:
            result: Result = await session.execute(stmt)
            return result.scalars().one()

    async def delete(self, id: int) -> bool:
        stmt = delete(self.DBModel).where(self.DBModel.id == id)
        async with self.get_session() as session:
            result: Result = await session.execute(stmt)
            return True
