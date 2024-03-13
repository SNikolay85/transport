import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


class Point(Base):
    __tablename__ = 'point'

    id_point = sq.Column(sq.Integer, primary_key=True)
    name_point = sq.Column(sq.String(length=100))
    cost = sq.Column(sq.Integer)

    def __str__(self):
        return f'Point {self.id_point}: ' \
               f'({self.name_point}, ' \
               f'{self.cost})'


class Route(Base):
    __tablename__ = 'route'

    id_route = sq.Column(sq.Integer, primary_key=True)
    id_start_route = sq.Column(sq.Integer, sq.ForeignKey('point.id_point'), nullable=False)
    id_finish_route = sq.Column(sq.Integer, sq.ForeignKey('point.id_point'), nullable=False)
    distance = sq.Column(sq.Integer)

    point_start = relationship(Point, backref='start_route', foreign_keys=[id_start_route])
    point_finish = relationship(Point, backref='finish_route', foreign_keys=[id_finish_route])

    def __str__(self):
        return f'Route {self.id_route}: ' \
               f'({self.id_start_route}, ' \
               f'{self.id_finish_route}, ' \
               f'{self.distance})'

class Fuel(Base):
    __tablename__ = 'fuel'

    id_fuel = sq.Column(sq.Integer, primary_key=True)
    name_fuel = sq.Column(sq.String(length=20))

    def __str__(self):
        return f'Fuel {self.id_fuel}: ' \
               f'{self.name_fuel})'


class Car(Base):
    __tablename__ = 'car'

    id_car = sq.Column(sq.Integer, primary_key=True)
    name_car = sq.Column(sq.String(length=40))
    number_of_car = sq.Column(sq.String(length=20))
    average_consumption = sq.Column(sq.Integer)


    def __str__(self):
        return f'Car {self.id_car}: ' \
               f'({self.name_car}, ' \
               f'{self.number_of_car}, ' \
               f'{self.average_consumption})'


class Car_Fuel(Base):
    __tablename__ = 'car_fuel'

    id_car_fuel = sq.Column(sq.Integer, primary_key=True)
    id_car = sq.Column(sq.Integer, sq.ForeignKey('car.id_car'), nullable=False)
    id_fuel = sq.Column(sq.Integer, sq.ForeignKey('fuel.id_fuel'), nullable=False)

    car = relationship(Car, backref='car_fuel')
    fuel = relationship(Fuel, backref='car_fuel')


    def __str__(self):
        return f'Car_Fuel {self.id_car_fuel}: ' \
               f'({self.id_car}, ' \
               f'{self.id_fuel})'

class Position(Base):
    __tablename__ = 'position'

    id_position = sq.Column(sq.Integer, primary_key=True)
    name_position = sq.Column(sq.String(length=50))

    def __str__(self):
        return f'Position {self.id_position}: ' \
               f'{self.name_position}'


class Where_drive(Base):
    __tablename__ = 'where_drive'

    id_wd = sq.Column(sq.Integer, primary_key=True)
    name_wd = sq.Column(sq.String(length=40))

    def __str__(self):
        return f'Where_drive {self.id_wd}: ' \
            f'{self.name_wd}'

class People(Base):
    __tablename__ = 'people'

    id_people = sq.Column(sq.Integer, primary_key=True)
    first_name = sq.Column(sq.String(length=20))
    last_name = sq.Column(sq.String(length=40))
    patronymic = sq.Column(sq.String(length=40))
    id_point = sq.Column(sq.Integer, sq.ForeignKey('point.id_point'), nullable=False)
    id_position = sq.Column(sq.Integer, sq.ForeignKey('position.id_position'), nullable=False)
    driving_licence = sq.Column(sq.String(length=30), unique=True, default=None)
    id_car = sq.Column(sq.Integer, sq.ForeignKey('car.id_car'), unique=True, default=None)

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
               f'{self.id_car})'


class Drivers(Base):
    __tablename__ = 'drivers'

    id_driver = sq.Column(sq.Integer, primary_key=True)
    driver = sq.Column(sq.Integer, sq.ForeignKey('people.id_people'), nullable=False)
    date = sq.Column(sq.Date, nullable=False)

    people = relationship(People, backref='drivers')

    def __str__(self):
        return f'Drivers {self.id_driver}: ' \
            f'({self.driver}, ' \
            f'{self.date})'


class Passengers(Base):
    __tablename__ = 'passengers'

    id_passenger = sq.Column(sq.Integer, primary_key=True)
    order = sq.Column(sq.Integer, nullable=False)
    passenger = sq.Column(sq.Integer, sq.ForeignKey('people.id_people'), nullable=False)
    driver = sq.Column(sq.Integer, sq.ForeignKey('drivers.id_driver'), nullable=False)
    id_where_drive = sq.Column(sq.Integer, sq.ForeignKey('where_drive.id_wd'), nullable=False)

    people = relationship(People, backref='passengers')
    drivers = relationship(Drivers, backref='passengers')
    where_drive = relationship(Where_drive, backref='passengers')


    def __str__(self):
        return f'Passengers {self.id_passenger}: ' \
            f'({self.order}, ' \
            f'{self.passenger}, ' \
            f'{self.driver}, ' \
            f'{self.id_where_drive})'


# created_on = sq.Column(sq.DateTime(), default=datetime.now)
# updated_on = sq.Column(sq.DateTime(), default=datetime.now, onupdate=datetime.now)

def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
