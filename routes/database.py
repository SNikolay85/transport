from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from config import PG_DB, PG_USER, PG_PASSWORD, PG_HOST, PG_PORT

PG_DSN = f"postgresql+asyncpg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"


engine = create_async_engine(PG_DSN)

new_session = async_sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()


class TaskOrm(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
