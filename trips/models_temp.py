from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

from config import PG_DB, PG_USER, PG_PASSWORD, PG_HOST, PG_PORT

PG_DSN = f"postgresql+asyncpg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"

engine = create_async_engine(PG_DSN, echo=True)

Session = async_sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()


class Point(Base):
    __tablename__ = 'point'

    id_point = Column(Integer, primary_key=True)
    name_point = Column(String(length=100))
    cost = Column(Integer)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    def __str__(self):
        return f'Point {self.id_point}: ' \
               f'({self.name_point}, ' \
               f'{self.cost}, ' \
               f'{self.created_on}, ' \
               f'{self.updated_on})'


class Route(Base):
    __tablename__ = 'route'

    id_route = Column(Integer, primary_key=True)
    id_start_route = Column(Integer, ForeignKey('point.id_point'), nullable=False)
    id_finish_route = Column(Integer, ForeignKey('point.id_point'), nullable=False)
    distance = Column(Integer)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    point_start = relationship(Point, backref='start_route', foreign_keys=[id_start_route])
    point_finish = relationship(Point, backref='finish_route', foreign_keys=[id_finish_route])

    def __str__(self):
        return f'Route {self.id_route}: ' \
               f'({self.id_start_route}, ' \
               f'{self.id_finish_route}, ' \
               f'{self.distance}, ' \
               f'{self.created_on}, ' \
               f'{self.updated_on})'


class Fuel(Base):
    __tablename__ = 'fuel'

    id_fuel = Column(Integer, primary_key=True)
    name_fuel = Column(String(length=20))
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    def __str__(self):
        return f'Fuel {self.id_fuel}: ' \
               f'{self.name_fuel}, ' \
               f'{self.created_on}, ' \
               f'{self.updated_on})'


class Car(Base):
    __tablename__ = 'car'

    id_car = Column(Integer, primary_key=True)
    name_car = Column(String(length=40))
    number_of_car = Column(String(length=20))
    average_consumption = Column(Integer)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    def __str__(self):
        return f'Car {self.id_car}: ' \
               f'({self.name_car}, ' \
               f'{self.number_of_car}, ' \
               f'{self.average_consumption}, ' \
               f'{self.created_on}, ' \
               f'{self.updated_on})'


class CarFuel(Base):
    __tablename__ = 'car_fuel'

    id_car_fuel = Column(Integer, primary_key=True)
    id_car = Column(Integer, ForeignKey('car.id_car'), nullable=False)
    id_fuel = Column(Integer, ForeignKey('fuel.id_fuel'), nullable=False)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    car = relationship(Car, backref='car_fuel')
    fuel = relationship(Fuel, backref='car_fuel')

    def __str__(self):
        return f'CarFuel {self.id_car_fuel}: ' \
               f'({self.id_car}, ' \
               f'{self.id_fuel}, ' \
               f'{self.created_on}, ' \
               f'{self.updated_on})'


class Position(Base):
    __tablename__ = 'position'

    id_position = Column(Integer, primary_key=True)
    name_position = Column(String(length=50))
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    def __str__(self):
        return f'Position {self.id_position}: ' \
               f'({self.name_position}, ' \
               f'{self.created_on}, ' \
               f'{self.updated_on})'


class WhereDrive(Base):
    __tablename__ = 'where_drive'

    id_wd = Column(Integer, primary_key=True)
    name_wd = Column(String(length=40))
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    def __str__(self):
        return f'WhereDrive {self.id_wd}: ' \
               f'({self.name_wd}, ' \
               f'{self.created_on}, ' \
               f'{self.updated_on})'


class People(Base):
    __tablename__ = 'people'

    id_people = Column(Integer, primary_key=True)
    first_name = Column(String(length=20))
    last_name = Column(String(length=40))
    patronymic = Column(String(length=40))
    id_point = Column(Integer, ForeignKey('point.id_point'), nullable=False)
    id_position = Column(Integer, ForeignKey('position.id_position'), nullable=False)
    driving_licence = Column(String(length=30), unique=True, default=None)
    id_car = Column(Integer, ForeignKey('car.id_car'), unique=True, default=None)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    point = relationship(Point, backref='people')
    position = relationship(Position, backref='people')
    car = relationship(Car, backref='people')

    def __str__(self):
        return f'People {self.id_people}: ' \
               f'({self.first_name}, ' \
               f'{self.last_name}, ' \
               f'{self.patronymic}, ' \
               f'{self.id_point}, ' \
               f'{self.id_position}, ' \
               f'{self.driving_licence}, ' \
               f'{self.id_car}, ' \
               f'{self.created_on}, ' \
               f'{self.updated_on})'


class Driver(Base):
    __tablename__ = 'driver'

    id_driver = Column(Integer, primary_key=True)
    driver = Column(Integer, ForeignKey('people.id_people'), nullable=False)
    date_trip = Column(Date, nullable=False)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    people = relationship(People, backref='drivers')

    def __str__(self):
        return f'Drivers {self.id_driver}: ' \
               f'({self.driver}, ' \
               f'{self.date_trip}, ' \
               f'{self.created_on}, ' \
               f'{self.updated_on})'


class Passenger(Base):
    __tablename__ = 'passenger'

    id_passenger = Column(Integer, primary_key=True)
    order = Column(Integer, nullable=False)
    passenger = Column(Integer, ForeignKey('people.id_people'), nullable=False)
    driver = Column(Integer, ForeignKey('driver.id_driver'), nullable=False)
    id_where_drive = Column(Integer, ForeignKey('where_drive.id_wd'), nullable=False)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    people = relationship(People, backref='passenger')
    drivers = relationship(Driver, backref='passenger')
    where_drive = relationship(WhereDrive, backref='passenger')

    def __str__(self):
        return f'Passengers {self.id_passenger}: ' \
               f'({self.order}, ' \
               f'{self.passenger}, ' \
               f'{self.driver}, ' \
               f'{self.id_where_drive}, ' \
               f'{self.created_on}, ' \
               f'{self.updated_on})'


async def delete_tables():
    async with engine.begin() as connect:
        await connect.run_sync(Base.metadata.drop_all)


async def create_tables():
    async with engine.begin() as connect:
        await connect.run_sync(Base.metadata.create_all)

# def create_tables(engine):
#     Base.metadata.drop_all(engine)
#     Base.metadata.create_all(engine)
