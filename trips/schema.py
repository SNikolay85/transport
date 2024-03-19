from datetime import date
from typing import Optional
from pydantic import BaseModel


class PointAdd(BaseModel):
    name_point: str
    cost: int


class FullPointAdd(PointAdd):
    id_point: int


class RouteAdd(BaseModel):
    id_start_route: int
    id_finish_route: int
    distance: int


class FullRouteAdd(RouteAdd):
    id_route: int


class FuelAdd(BaseModel):
    name_fuel: str


class FullFuelAdd(FuelAdd):
    id_fuel: int


class CarAdd(BaseModel):
    name_car: str
    number_of_car: str
    average_consumption: int


class FullCarAdd(CarAdd):
    id_car: int


class CarFuelAdd(BaseModel):
    id_car: int
    id_fuel: int


class FullCarFuelAdd(CarFuelAdd):
    id_car_fuel: int


class PositionAdd(BaseModel):
    name_position: str


class FullPositionAdd(PositionAdd):
    id_position: int


class WhereDriveAdd(BaseModel):
    name_wd: str


class FullWhereDriveAdd(WhereDriveAdd):
    id_wd: int


class PeopleAdd(BaseModel):
    first_name: str
    last_name: str
    patronymic: str
    id_point: int
    id_position: int
    driving_licence: str
    id_car: int


class FullPeopleAdd(PeopleAdd):
    id_people: int


class DriverAdd(BaseModel):
    driver: int
    date_trip: date


class FullDriverAdd(DriverAdd):
    id_driver: int


class PassengerAdd(BaseModel):
    order: int
    passenger: int
    driver: int
    id_where_drive: int


class FullPassengerAdd(PassengerAdd):
    id_passenger: int

