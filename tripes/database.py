from typing import Optional

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy import Integer, Column, String
from config import PG_DB, PG_USER, PG_PASSWORD, PG_HOST, PG_PORT

PG_DSN = f"postgresql+asyncpg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"


engine = create_async_engine(PG_DSN)

new_session = async_sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()


class TaskOrm(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[Optional[str]]

    # id = Column(Integer, primary_key=True)
    # name = Column(String(length=100))
    # description = Column(String(length=255), nullable=True, default=None)


async def delete_tables():
    async with engine.begin() as connect:
        await connect.run_sync(Base.metadata.drop_all)


async def create_tables():
    async with engine.begin() as connect:
        await connect.run_sync(Base.metadata.create_all)
