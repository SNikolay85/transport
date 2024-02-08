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
               f'({self.name_point},' \
               f'{self.cost})'


class Route(Base):
    __tablename__ = 'route'

    id_route = sq.Column(sq.Integer, primary_key=True)
    id_start_route = sq.Column(sq.Integer, sq.ForeignKey('point.id_point'), nullable=False)
    id_finish_route = sq.Column(sq.Integer, sq.ForeignKey('point.id_point'), nullable=False)
    distance = sq.Column(sq.Integer)

    point = relationship(Point, backref='route')

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
               f'{self.number_of_car},' \
               f'{self.average_consumption},' \
               f'{self.id_fuel})'


class Car_Fuel(Base):
    __tablename__ = 'car_fuel'

    id_car_fuel = sq.Column(sq.Integer, primary_key=True)
    id_car = sq.Column(sq.Integer, sq.ForeignKey('car.id_car'), nullable=False)
    id_fuel = sq.Column(sq.Integer, sq.ForeignKey('fuel.id_fuel'), nullable=False)

    car = relationship(Car, backref='car_fuel')
    fuel = relationship(Fuel, backref='car_fuel')

class Position(Base):
    __tablename__ = 'position'

    id_position = sq.Column(sq.Integer, primary_key=True)
    name_position = sq.Column(sq.String(length=50))

    def __str__(self):
        return f'Position {self.id_position}: ' \
               f'{self.name_position},' \

class People(Base):
    __tablename__ = 'people'

    id_people = sq.Column(sq.Integer, primary_key=True)
    first_name = sq.Column(sq.String(length=20))
    last_name = sq.Column(sq.String(length=40))
    patronymic = sq.Column(sq.String(length=40))
    id_point = sq.Column(sq.Integer, sq.ForeignKey('point.id_point'), nullable=False)
    id_position = sq.Column(sq.Integer, sq.ForeignKey('position.id_position'), nullable=False)
    driving_licence = sq.Column(sq.String(length=30))
    id_car = sq.Column(sq.Integer, sq.ForeignKey('car.id_car'), nullable=False)

    point = relationship(Point, backref='point')
    position = relationship(Position, backref='position')
    car = relationship(Car, backref='people')

    def __str__(self):
        return f'People {self.id_people}: ' \
               f'({self.first_name}, ' \
               f'{self.last_name},' \
               f'{self.patronymic},' \
               f'{self.id_point},' \
               f'{self.id_position},' \
               f'{self.driving_licence},' \
               f'{self.id_car})'

class Transport(Base):
    __tablename__ = 'main_table'

    id_transport = sq.Column(sq.Integer, primary_key=True)
    id_people = sq.Column(sq.Integer, sq.ForeignKey('people.id_people'), nullable=False)
    day_of_date = sq.Column(sq.Date)
    id_route = sq.Column(sq.Integer, sq.ForeignKey('route.id_route'), nullable=False)
    man_to_job = sq.Column(sq.Integer)
    man_with_job = sq.Column(sq.Integer)
    created_on = sq.Column(sq.DateTime(), default=datetime.now)
    updated_on = sq.Column(sq.DateTime(), default=datetime.now, onupdate=datetime.now)

    people = relationship(People, backref='main_table')
    route = relationship(Route, backref='main_table')

    def __str__(self):
        return f'Transport {self.id_transport}: ' \
               f'({self.id_people},' \
               f'{self.day_of_date},' \
               f'{self.id_route},' \
               f'{self.created_on},' \
               f'{self.updated_on})'


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)