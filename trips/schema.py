from datetime import date
from typing import Optional
from pydantic import BaseModel

from trips.models import Fuel, WhereDrive


class PointAdd(BaseModel):
    name_point: str
    cost: int


class FullPoint(PointAdd):
    id_point: int


class RouteAdd(BaseModel):
    id_start_point: int
    id_finish_point: int
    distance: int


class FullRoute(RouteAdd):
    id_route: int


class CarAdd(BaseModel):
    name_car: str
    number_of_car: str
    average_consumption: int
    id_people: int


class FullCar(CarAdd):
    id_car: int


class CarFuelAdd(BaseModel):
    id_car: int
    fuel: Fuel


class FullCarFuel(CarFuelAdd):
    id_car_fuel: int


class PositionAdd(BaseModel):
    name_position: str


class FullPosition(PositionAdd):
    id_position: int


class PeopleAdd(BaseModel):
    first_name: str
    last_name: str
    patronymic: str
    id_point: int
    id_position: int
    driving_licence: Optional[str]


class FullPeople(PeopleAdd):
    id_people: int


class DriverAdd(BaseModel):
    id_people: int
    date_trip: date


class FullDriver(DriverAdd):
    id_driver: int


class PassengerAdd(BaseModel):
    order: int
    id_people: int
    id_driver: int
    where_drive: WhereDrive


class FullPassenger(PassengerAdd):
    id_passenger: int


class FullPointRe(FullPoint):
    peoples: list['FullPeople']


class FullRouteRe(FullRoute):
    point_start: 'FullPoint'
    point_finish: 'FullPoint'


class FullCarRe(FullCar):
    people: 'FullPeople'


class FullPositionRe(FullPosition):
    peoples: list['FullPeople']


class FullPeopleRe(FullPeople):
    point: 'FullPoint'
    position: 'FullPosition'
    cars: list['FullCar']


class FullDriverRe(FullDriver):
    people: 'FullPeople'


class FullPassengerRe(FullPassenger):
    people: 'FullPeople'
    driver: 'FullDriverRe'
