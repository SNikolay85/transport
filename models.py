import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Point(Base):
    __tablename__ = 'point'

    id_point = sq.Column(sq.Integer, primary_key=True)
    name_point = sq.Column(sq.String(length=100))
    date_of_creation = sq.Column(sq.DateTime)

    def __str__(self):
        return f'Point {self.id_point}: ' \
               f'({self.name_point}, ' \
               f'{self.date_of_creation})'

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


class Transport(Base):
    __tablename__ = 'main_table'

    id = sq.Column(sq.Integer, primary_key=True)
    first_name = sq.Column(sq.String(length=20))
    last_name = sq.Column(sq.String(length=40))
    patronymic = sq.Column(sq.String(length=40))
    day_of_date = sq.Column(sq.Date)
    number_of_liters = sq.Column(sq.Integer)
    number_of_money = sq.Column(sq.Integer)
    id_route = sq.Column(sq.Integer, sq.ForeignKey('route.id_route'), nullable=False)
    distance = sq.Column(sq.Integer)
    man_to_job = sq.Column(sq.Integer)
    man_with_job = sq.Column(sq.Integer)

    route = relationship(Route, backref='main_table')

    def __str__(self):
        return f'Transport {self.day_of_date}: ({self.first_name}, {self.last_name})'

