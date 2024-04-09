from typing import Optional

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import String, ForeignKey, MetaData, Date, DateTime, TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, relationship, mapped_column, Mapped
from sqlalchemy.sql import func
from datetime import datetime, date

from typing_extensions import Annotated

from config import PG_DB, PG_USER, PG_PASSWORD, PG_HOST, PG_PORT

PG_DSN = f"postgresql+asyncpg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/test"

engine = create_async_engine(PG_DSN, echo=True)

Session = async_sessionmaker(engine, expire_on_commit=False)

my_metadata = MetaData()

intpk = Annotated[int, mapped_column(primary_key=True)]
#point_fk = Annotated[int, mapped_column(ForeignKey('point.id_point'))]
# car_fk = Annotated[int, mapped_column(ForeignKey('car.id_car'))]
# fuel_fk = Annotated[int, mapped_column(ForeignKey('fuel.id_fuel'))]
# position_fk = Annotated[int, mapped_column(ForeignKey('position.id_position'))]
# people_fk = Annotated[int, mapped_column(ForeignKey('people.id_people'))]
# driver_fk = Annotated[int, mapped_column(ForeignKey('driver.id_driver'))]
# wd_fk = Annotated[int, mapped_column(ForeignKey('where_drive.id_wd'))]
# str100 = Annotated[str, 100]
# str20 = Annotated[str, 20]
# str50 = Annotated[str, 50]
# date_trip = Annotated[date, mapped_column(Date)]
#
# created_on = Annotated[datetime, mapped_column(DateTime(timezone=True), server_default=func.now())]
# updated_on = Annotated[datetime, mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())]


class Base(DeclarativeBase):
    metadata = my_metadata
    # type_annotation_map = {
    #     str100: String(100),
    #     str20: String(20),
    #     str50: String(50),
    # }


class Point(Base):
    __tablename__ = 'point'

    id_point: Mapped[intpk]
    name_point: Mapped[str] = mapped_column(unique=True)
    cost: Mapped[int]
    # These are considered `separate` from the relationships on Route so you have to set the fks here too.
    start_for_routes: Mapped[list['Route']] = relationship(back_populates='point_start',
                                                           foreign_keys='[Route.id_start_point]')
    finish_for_routes: Mapped[list['Route']] = relationship(back_populates='point_finish',
                                                            foreign_keys='[Route.id_finish_point]')


class Route(Base):
    __tablename__ = 'route'

    id_route: Mapped[intpk]
    id_start_point: Mapped[int] = mapped_column(ForeignKey('point.id_point'))
    id_finish_point: Mapped[int] = mapped_column(ForeignKey('point.id_point'))
    distance: Mapped[int]


    # You can pass in the column in class scope OR...
    point_start: Mapped['Point'] = relationship(back_populates='start_for_routes', foreign_keys=id_start_point)
    # You can use the delayed resolution here too but you have to start with at least a class.
    point_finish: Mapped['Point'] = relationship(back_populates='finish_for_routes',
                                                 foreign_keys='[Route.id_finish_point]')


async def delete_tables():
    async with engine.begin() as connect:
        await connect.run_sync(Base.metadata.drop_all)


async def create_tables():
    async with engine.begin() as connect:
        await connect.run_sync(Base.metadata.create_all)