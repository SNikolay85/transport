from time import timezone
from typing import Optional

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy import Float, String, ForeignKey, MetaData, Date, DateTime, UniqueConstraint, create_engine
from sqlalchemy.orm import DeclarativeBase, relationship, mapped_column, Mapped, sessionmaker
from sqlalchemy.sql import func
from datetime import datetime, date

from typing_extensions import Annotated

from config import PG_DB, REAL_DB, PG_USER, PG_PASSWORD, PG_HOST, PG_PORT

# connection for the test base
SYNC_PG_DSN = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{REAL_DB}"
# connection for the real base
PG_DSN = f"postgresql+asyncpg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{REAL_DB}"

engine = create_async_engine(PG_DSN, echo=True)
sync_engine = create_engine(SYNC_PG_DSN)

Session = async_sessionmaker(engine, expire_on_commit=False)
Session_sync = sessionmaker(bind=sync_engine)

my_metadata = MetaData()

intpk = Annotated[int, mapped_column(primary_key=True)]
point_fk = Annotated[int, mapped_column(ForeignKey('point.id_point', ondelete="CASCADE"))]
car_fk = Annotated[int, mapped_column(ForeignKey('car.id_car', ondelete="CASCADE"))]
fuel_fk = Annotated[int, mapped_column(ForeignKey('fuel.id_fuel', ondelete="CASCADE"))]
wd_fk = Annotated[int, mapped_column(ForeignKey('where_drive.id_wd', ondelete="CASCADE"))]
position_fk = Annotated[int, mapped_column(ForeignKey('position.id_position', ondelete="CASCADE"))]
people_fk = Annotated[int, mapped_column(ForeignKey('people.id_people', ondelete="CASCADE"))]
organization_fk = Annotated[int, mapped_column(ForeignKey('organization.id_organization', ondelete="CASCADE"))]
driver_fk = Annotated[int, mapped_column(ForeignKey('driver.id_driver', ondelete="CASCADE"))]
role_fk = Annotated[int, mapped_column(ForeignKey('role.id_role', ondelete="CASCADE"))]
str100 = Annotated[str, 100]
str20 = Annotated[str, 20]
str50 = Annotated[str, 50]
date_trip = Annotated[date, mapped_column(Date)]
date_refueling = Annotated[datetime, mapped_column(DateTime)]

created_on = Annotated[datetime, mapped_column(DateTime(timezone=True), server_default=func.now())]
updated_on = Annotated[datetime, mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())]


class Base(DeclarativeBase):
    metadata = my_metadata
    type_annotation_map = {
        str100: String(100),
        str20: String(20),
        str50: String(50),
    }

    repr_cols_num = 2
    repr_cols = tuple()

    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f'{col}={getattr(self, col)}')
        return f'<{self.__class__.__name__} {", ".join(cols)}>'


class Point(Base):
    __tablename__ = 'point'

    id_point: Mapped[intpk]
    name_point: Mapped[str100] = mapped_column(unique=True)
    latitude: Mapped[float] = mapped_column(Float, nullable=True)
    longitude: Mapped[float] = mapped_column(Float, nullable=True)
    cost: Mapped[int]

    created_on: Mapped[created_on]
    updated_on: Mapped[updated_on]

    start_point: Mapped[list['Route']] = relationship(back_populates='point_start',
                                                      foreign_keys='[Route.id_start_point]')
    finish_point: Mapped[list['Route']] = relationship(back_populates='point_finish',
                                                       foreign_keys='[Route.id_finish_point]')
    peoples: Mapped[list['People']] = relationship(back_populates='point')
    organizations: Mapped[list['Organization']] = relationship(back_populates='point')

    peoples_driving_licence: Mapped[list['People']] = relationship(
        back_populates='point',
        primaryjoin='and_(Point.id_point == People.id_point, People.driving_licence != None)',
        order_by='People.last_name.desc()'
    )

    repr_cols_num = 5
    repr_cols = tuple()


class Route(Base):
    __tablename__ = 'route'

    id_route: Mapped[intpk]
    id_start_point: Mapped[point_fk]
    id_finish_point: Mapped[point_fk]
    distance: Mapped[int]
    __table_args__ = (UniqueConstraint('id_start_point', 'id_finish_point', name='start_finish_uc'),)

    created_on: Mapped[created_on]
    updated_on: Mapped[updated_on]

    point_start: Mapped[Point] = relationship(back_populates='start_point', foreign_keys='[Route.id_start_point]')
    point_finish: Mapped[Point] = relationship(back_populates='finish_point', foreign_keys='[Route.id_finish_point]')

    repr_cols_num = 4
    repr_cols = tuple()


class Fuel(Base):
    __tablename__ = 'fuel'

    id_fuel: Mapped[intpk]
    name_fuel: Mapped[str100] = mapped_column(unique=True)

    created_on: Mapped[created_on]
    updated_on: Mapped[updated_on]

    car_fuels: Mapped[list['CarFuel']] = relationship(back_populates='fuel')
    refuelings: Mapped[list['Refueling']] = relationship(back_populates='fuel')


class Car(Base):
    __tablename__ = 'car'

    id_car: Mapped[intpk]
    name_car: Mapped[str100]
    number_of_car: Mapped[str20] = mapped_column(unique=True)
    average_consumption: Mapped[int]
    id_people: Mapped[people_fk]

    created_on: Mapped[created_on]
    updated_on: Mapped[updated_on]

    car_fuels: Mapped[list['CarFuel']] = relationship(back_populates='car')
    people: Mapped['People'] = relationship(back_populates='cars')

    repr_cols_num = 5
    repr_cols = tuple()


class CarFuel(Base):
    __tablename__ = 'car_fuel'

    id_car_fuel: Mapped[intpk]
    id_car: Mapped[car_fk]
    id_fuel: Mapped[fuel_fk]
    __table_args__ = (UniqueConstraint('id_car', 'id_fuel', name='car_fuel_uc'),)

    created_on: Mapped[created_on]
    updated_on: Mapped[updated_on]

    car: Mapped['Car'] = relationship(back_populates='car_fuels')
    fuel: Mapped['Fuel'] = relationship(back_populates='car_fuels')

    repr_cols_num = 3
    repr_cols = tuple()


class Position(Base):
    __tablename__ = 'position'

    id_position: Mapped[intpk]
    name_position: Mapped[str100] = mapped_column(unique=True)

    created_on: Mapped[created_on]
    updated_on: Mapped[updated_on]

    peoples: Mapped[list['People']] = relationship(back_populates='position')


class WhereDrive(Base):
    __tablename__ = 'where_drive'

    id_wd: Mapped[intpk]
    name_wd: Mapped[str100] = mapped_column(unique=True)

    created_on: Mapped[created_on]
    updated_on: Mapped[updated_on]

    drivers: Mapped[list['Driver']] = relationship(back_populates='wd')
    passengers: Mapped[list['Passenger']] = relationship(back_populates='wd')
    other_routes: Mapped[list['OtherRoute']] = relationship(back_populates='wd')


class People(Base):
    __tablename__ = 'people'

    id_people: Mapped[intpk]
    first_name: Mapped[str50]
    last_name: Mapped[str50]
    patronymic: Mapped[str50]
    id_point: Mapped[point_fk]
    id_position: Mapped[position_fk]
    driving_licence: Mapped[Optional[str50]] = mapped_column(unique=True)
    ppr_card: Mapped[Optional[str]] = mapped_column(unique=True)
    __table_args__ = (UniqueConstraint('first_name', 'last_name', 'patronymic', 'id_point', 'id_position', name='people_uc'),)

    created_on: Mapped[created_on]
    updated_on: Mapped[updated_on]

    point: Mapped['Point'] = relationship(back_populates='peoples')
    position: Mapped['Position'] = relationship(back_populates='peoples')
    cars: Mapped[list['Car']] = relationship(back_populates='people')
    drivers: Mapped[list['Driver']] = relationship(back_populates='people')
    passengers: Mapped[list['Passenger']] = relationship(back_populates='people')
    refuelings: Mapped[list['Refueling']] = relationship(back_populates='people')
    identification: Mapped['IdentificationUser'] = relationship(back_populates='people')

    repr_cols_num = 7
    repr_cols = tuple()


class IdentificationUser(Base):
    __tablename__ = 'identification'

    id_identification: Mapped[intpk]
    id_people: Mapped[people_fk]
    id_tg: Mapped[Optional[str50]] = mapped_column(unique=True)
    login: Mapped[Optional[str50]] = mapped_column(unique=True)
    password: Mapped[Optional[str50]] = mapped_column(unique=True)
    id_role: Mapped[role_fk]
    __table_args__ = (UniqueConstraint('id_people', 'id_tg', 'login', 'password', 'id_role', name='identification_uc'),)

    created_on: Mapped[created_on]
    updated_on: Mapped[updated_on]

    people: Mapped['People'] = relationship(back_populates='identification')
    role: Mapped['Role'] = relationship(back_populates='identifications')

    repr_cols_num = 6
    repr_cols = tuple()


class Role(Base):
    __tablename__ = 'role'

    id_role: Mapped[intpk]
    name_role: Mapped[str50] = mapped_column(unique=True)

    created_on: Mapped[created_on]
    updated_on: Mapped[updated_on]

    identifications: Mapped[list['IdentificationUser']] = relationship(back_populates='role')

    repr_cols_num = 2
    repr_cols = tuple()


class Organization(Base):
    __tablename__ = 'organization'

    id_organization: Mapped[intpk]
    name_organization: Mapped[str50]
    id_point: Mapped[point_fk]
    __table_args__ = (UniqueConstraint('name_organization', 'id_point', name='organization_uc'),)

    created_on: Mapped[created_on]
    updated_on: Mapped[updated_on]

    point: Mapped['Point'] = relationship(back_populates='organizations')
    other_routes: Mapped[list['OtherRoute']] = relationship(back_populates='organization')

    repr_cols_num = 3
    repr_cols = tuple()


class Driver(Base):
    __tablename__ = 'driver'

    id_driver: Mapped[intpk]
    id_people: Mapped[people_fk]
    date_trip: Mapped[date_trip]
    where_drive: Mapped[wd_fk]
    __table_args__ = (UniqueConstraint('id_driver', 'id_people', 'date_trip', name='people_date_uc'),)

    created_on: Mapped[created_on]
    updated_on: Mapped[updated_on]

    people: Mapped['People'] = relationship(back_populates='drivers')
    passengers: Mapped[list['Passenger']] = relationship(back_populates='driver')
    other_routes: Mapped[list['OtherRoute']] = relationship(back_populates='driver')
    wd: Mapped['WhereDrive'] = relationship(back_populates='drivers')

    repr_cols_num = 4
    repr_cols = tuple('created_on', )


class Passenger(Base):
    __tablename__ = 'passenger'

    id_passenger: Mapped[intpk]
    order: Mapped[int]
    id_people: Mapped[people_fk]
    id_driver: Mapped[driver_fk]
    where_drive: Mapped[wd_fk]
    __table_args__ = (UniqueConstraint('id_people', 'id_driver', 'where_drive', name='passenger_uc'),)

    created_on: Mapped[created_on]
    updated_on: Mapped[updated_on]

    people: Mapped['People'] = relationship(back_populates='passengers')
    driver: Mapped['Driver'] = relationship(back_populates='passengers')
    wd: Mapped['WhereDrive'] = relationship(back_populates='passengers')

    repr_cols_num = 5
    repr_cols = tuple('created_on', )


class OtherRoute(Base):
    __tablename__ = 'other_route'

    id_other_route: Mapped[intpk]
    order: Mapped[int]
    id_organization: Mapped[organization_fk]
    id_driver: Mapped[driver_fk]
    where_drive: Mapped[wd_fk]
    __table_args__ = (UniqueConstraint('id_organization', 'id_driver', 'where_drive', name='other_route_uc'),)

    created_on: Mapped[created_on]
    updated_on: Mapped[updated_on]

    organization: Mapped['Organization'] = relationship(back_populates='other_routes')
    driver: Mapped['Driver'] = relationship(back_populates='other_routes')
    wd: Mapped['WhereDrive'] = relationship(back_populates='other_routes')

    repr_cols_num = 5
    repr_cols = tuple('created_on', )


class Refueling(Base):
    __tablename__ = 'refueling'

    id_refueling: Mapped[intpk]
    id_fuel: Mapped[fuel_fk]
    id_people: Mapped[people_fk]
    quantity: Mapped[float] = mapped_column(Float(precision=2, asdecimal=2,decimal_return_scale=2), nullable=False)
    date_refueling: Mapped[date_refueling]
    __table_args__ = (UniqueConstraint('id_fuel', 'id_people', 'quantity', 'date_refueling', name='refueling_uc'),)

    created_on: Mapped[created_on]
    updated_on: Mapped[updated_on]

    fuel: Mapped['Fuel'] = relationship(back_populates='refuelings')
    people: Mapped['People'] = relationship(back_populates='refuelings')

    repr_cols_num = 5
    repr_cols = tuple('created_on', )


async def delete_tables():
    async with engine.begin() as connect:
        await connect.run_sync(Base.metadata.drop_all)


async def create_tables():
    async with engine.begin() as connect:
        await connect.run_sync(Base.metadata.create_all)
