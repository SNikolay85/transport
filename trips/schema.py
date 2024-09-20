from datetime import date, datetime
from typing import Optional, Any

from pydantic import BaseModel, Field, field_validator
from pydantic.main import Model
from sqlalchemy import func

'''
gt - больше, чем
lt - меньше, чем
ge - больше или равно
le - меньше или равно
multiple_of - кратно заданному числу
allow_inf_nan - разрешать 'inf', '-inf', 'nan' значения
'''


# --------------------------
# schemes for model Point
class PointAdd(BaseModel):
    name_point: str = Field(max_length=100, min_length=1)
    cost: int = Field(ge=0)


class FullPoint(PointAdd):
    id_point: int
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class AllRecordsPoint(FullPoint):
    create_on: datetime
    update_on: datetime


class NamePoint(BaseModel):
    id_point: int
    name_point: str


class FullPointRe(FullPoint):
    peoples: list['FullPeople']


class PointDrivingLicenceRe(FullPoint):
    peoples_driving_licence: list['FullPeople']


class PointMin(BaseModel):
    name_point: str


# --------------------------
# schemes for model Fuel
class FuelAdd(BaseModel):
    name_fuel: str


class FullFuel(FuelAdd):
    id_fuel: int


# class AllRecordsFuel(FullFuel):
#     create_on: datetime
#     update_on: datetime


class FullFuelRe(FullFuel):
    refuelings: list['FullRefueling']


# --------------------------
# schemes for model WhereDrive
class WhereDriveAdd(BaseModel):
    name_wd: str


class FullWhereDrive(WhereDriveAdd):
    id_wd: int


# class AllRecordsWhereDrive(FullWhereDrive):
#     create_on: datetime
#     update_on: datetime


class FullWhereDriveRe(FullWhereDrive):
    passengers: list['FullPassenger']


# --------------------------
# schemes for model CarFuel
class CarFuelAdd(BaseModel):
    id_car: int
    id_fuel: int


class FullCarFuel(CarFuelAdd):
    id_car_fuel: int


# class AllRecordsCarFuel(FullCarFuel):
#     create_on: datetime.tzinfo
#     update_on: datetime


# --------------------------
# schemes for model People
class PeopleAdd(BaseModel):
    first_name: str
    last_name: str
    patronymic: str
    id_point: int
    id_position: int
    driving_licence: Optional[str] = None


class PeopleMin(BaseModel):
    first_name: str
    last_name: str


class FullPeople(PeopleAdd):
    id_people: int


# class AllRecordsPeople(FullPeople):
#     create_on: datetime
#     update_on: datetime


class FullPeopleRe(FullPeople):
    point: 'PointMin'
    position: 'FullPosition'
    cars: list['FullCar']


class FullPeRe(FullPeople):
    point: 'FullPoint'
    position: 'FullPosition'
    cars: list['FullCar']


# --------------------------
# schemes for model Organization
class OrganizationAdd(BaseModel):
    name_organization: str
    id_point: int


class OrganizationUpdate(BaseModel):
    name_organization: Optional[str] = None
    id_point: Optional[int] = None


class FullOrganization(OrganizationAdd):
    id_organization: int


# class AllRecordsOrganization(FullOrganization):
#     create_on: datetime
#     update_on: datetime


class FullOrganizationRe(FullOrganization):
    point: 'PointMin'


# --------------------------
# schemes for model Car
class CarAdd(BaseModel):
    name_car: str
    number_of_car: str
    average_consumption: int
    id_people: int


class FullCar(CarAdd):
    id_car: int


# class AllRecordsCar(FullCar):
#     create_on: datetime
#     update_on: datetime


class FullCarRe(FullCar):
    people: 'FullPeople'


# --------------------------
# schemes for model Driver
class DriverAdd(BaseModel):
    id_people: int
    date_trip: date


class FullDriver(DriverAdd):
    id_driver: int


# class AllRecordsDriver(FullDriver):
#     create_on: datetime.tzinfo
#     update_on: datetime.tzinfo


class FullDriverRe(FullDriver):
    people: 'FullPeople'


# --------------------------
# schemes for model Passenger
class PassengerAdd(BaseModel):
    order: int
    id_people: int
    id_driver: int
    where_drive: int


class FullPassenger(PassengerAdd):
    id_passenger: int


# class AllRecordsPassenger(FullPassenger):
#     create_on: datetime.tzinfo
#     update_on: datetime.tzinfo


class FullPassengerRe(FullPassenger):
    people: 'PeopleMin'
    driver: 'FullDriver'
    wd: 'FullWhereDrive'


class FullPassengerDriverRe(FullPassenger):
    people: 'FullPeople'
    driver: 'FullDriver'


# --------------------------
# schemes for model OtherRoute
class OtherRouteAdd(BaseModel):
    order: int
    id_organization: int
    id_driver: int
    where_drive: int


class FullOtherRoute(OtherRouteAdd):
    id_other_route: int


# class AllRecordsOtherRoute(FullOtherRoute):
#     create_on: datetime.tzinfo
#     update_on: datetime.tzinfo


class FullOtherRouteRe(FullOtherRoute):
    organization: 'FullOrganization'
    driver: 'FullDriver'
    wd: 'FullWhereDrive'


# --------------------------
# schemes for model Position
class PositionAdd(BaseModel):
    name_position: str


class FullPosition(PositionAdd):
    id_position: int


# class AllRecordsPosition(FullPosition):
#     create_on: datetime.tzinfo
#     update_on: datetime.tzinfo


class FullPositionRe(FullPosition):
    peoples: list['FullPeople']


# --------------------------
# schemes for model Route
class RouteAdd(BaseModel):
    id_start_point: int
    id_finish_point: int


class FullRoute(RouteAdd):
    id_route: int
    distance: Optional[int] = None


# class AllRecordsRoute(FullRoute):
#     create_on: datetime.tzinfo
#     update_on: datetime.tzinfo


class FullRouteRe(FullRoute):
    point_start: 'FullPoint'
    point_finish: 'FullPoint'


# --------------------------
# schemes for model Refueling
class RefuelingAdd(BaseModel):
    id_fuel: int
    id_people: int
    quantity: float
    date_refueling: date


class FullRefueling(RefuelingAdd):
    id_refueling: int


# class AllRecordsRefueling(FullRefueling):
#     create_on: datetime.tzinfo
#     update_on: datetime.tzinfo


class FullRefuelingRe(FullRefueling):
    fuel: 'FullFuel'
    people: 'FullPeople'
