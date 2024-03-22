from datetime import datetime
from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy import Boolean, String, DateTime, ForeignKey, Integer
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from config import PG_USER, PG_PASSWORD, PG_HOST, PG_PORT, PG_DB

PG_DSN = f"postgresql+asyncpg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"


class Base(DeclarativeBase):
    pass


class User(SQLAlchemyBaseUserTable[int], Base):
    id_people: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(length=20))
    last_name: Mapped[str] = mapped_column(String(length=40))
    patronymic: Mapped[str] = mapped_column(String(length=40))
    id_point: Mapped[int] = mapped_column(Integer, ForeignKey('point.c.id_point'), nullable=False)
    id_position: Mapped[int] = mapped_column(Integer, ForeignKey('position.c.id_position'), nullable=False)
    driving_licence: Mapped[str] = mapped_column(String(length=30), unique=True, default=None)
    id_car: Mapped[int] = mapped_column(Integer, ForeignKey('car.c.id_car'), unique=True, default=None)
    created_on:Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_on: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)
    email: Mapped[str] = mapped_column(String(length=320), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


engine = create_async_engine(PG_DSN)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
