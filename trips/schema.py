from datetime import date, datetime
from typing import Optional, Any

from pydantic import BaseModel, Field, field_validator

from trips.models import Point, Session
from sqlalchemy import func, select

'''
gt - больше, чем
lt - меньше, чем
ge - больше или равно
le - меньше или равно
multiple_of - кратно заданному числу
allow_inf_nan - разрешать 'inf', '-inf', 'nan' значения
'''


class Utils:
    @staticmethod
    def find_all_point():
        with Session() as session:
            query = select(Point.id_point)
            result = session.execute(query)
            models = result.unique().scalars().all()
            return models


# --------------------------
# schemes for model Point
class PointAdd(BaseModel):
    name_point: str = Field(max_length=100, min_length=1)
    cost: int = Field(ge=0)


class PointUpdate(BaseModel):
    name_point: Optional[str] = Field(default=None, max_length=100, min_length=1)
    cost: Optional[int] = Field(default=None, ge=0)


class FullPoint(PointAdd):
    id_point: int
    latitude: Optional[float] = None
    longitude: Optional[float] = None


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


class FullFuelRe(FullFuel):
    refuelings: list['FullRefueling']


# --------------------------
# schemes for model WhereDrive
class WhereDriveAdd(BaseModel):
    name_wd: str


class FullWhereDrive(WhereDriveAdd):
    id_wd: int


class FullWhereDriveRe(FullWhereDrive):
    passengers: list['FullPassenger']
    other_routes: list['FullOtherRoute']
    drivers: list['FullDriver']


# --------------------------
# schemes for model CarFuel
class CarFuelAdd(BaseModel):
    id_car: int
    id_fuel: int


class FullCarFuel(CarFuelAdd):
    id_car_fuel: int


# --------------------------
# schemes for model People
class PeopleAdd(BaseModel):
    first_name: str
    last_name: str
    patronymic: str
    id_point: int
    id_position: int
    driving_licence: Optional[str] = None
    ppr_card: Optional[str] = None


class PeopleMin(BaseModel):
    first_name: str
    last_name: str


class FullPeople(PeopleAdd):
    id_people: int


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

    # @field_validator('id_point')
    # async def validate(self, id_point):
    #     if id_point not in [i.id_organization for i in await DataGet.find_all_organization()]:
    #         raise ValueError('such id not in base')
    #     return id_point


class OrganizationUpdate(BaseModel):
    name_organization: Optional[str] = None
    id_point: Optional[int] = None

    # @field_validator('name_organization', 'id_point')
    # @classmethod
    # def valid(cls, a, b):
    #     if a is None and b is None:
    #         raise ValueError('xren')
    #     return a, b
    # @field_validator('id_point')
    # @classmethod
    # def validate(cls, id_point):
    #     if id_point not in [1, 3, 6]:
    #         raise ValueError('such id not in base')
    #     return id_point


class FullOrganization(OrganizationAdd):
    id_organization: int


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


class FullCarRe(FullCar):
    people: 'FullPeople'


# --------------------------
# schemes for model Driver
class DriverAdd(BaseModel):
    id_people: int
    date_trip: date
    where_drive: int


class FullDriver(DriverAdd):
    id_driver: int


class FullDriverRe(FullDriver):
    people: 'FullPeople'
    wd: 'FullWhereDrive'


# --------------------------
# schemes for model Passenger
class PassengerAdd(BaseModel):
    order: int
    id_people: int
    id_driver: int
    where_drive: int


class FullPassenger(PassengerAdd):
    id_passenger: int


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


class FullOtherRouteRe(FullOtherRoute):
    organization: 'FullOrganization'
    driver: 'FullDriver'
    wd: 'FullWhereDrive'


class FullOtherRouteDriverRe(FullOtherRoute):
    organization: 'FullOrganization'
    driver: 'FullDriver'


# --------------------------
# schemes for model Position
class PositionAdd(BaseModel):
    name_position: str


class FullPosition(PositionAdd):
    id_position: int


class FullPositionRe(FullPosition):
    peoples: list['FullPeople']


# --------------------------
# schemes for model Route
class RouteAdd(BaseModel):
    id_start_point: int
    id_finish_point: int
    distance: Optional[int] = None


class FullRoute(RouteAdd):
    id_route: int


class RouteUpdate(BaseModel):
    distance: Optional[int] = None


class FullRouteRe(FullRoute):
    point_start: 'FullPoint'
    point_finish: 'FullPoint'


# --------------------------
# schemes for model Refueling
class RefuelingAdd(BaseModel):
    id_fuel: int
    id_people: int
    quantity: float
    date_refueling: datetime


class FullRefueling(RefuelingAdd):
    id_refueling: int


class FullRefuelingRe(FullRefueling):
    fuel: 'FullFuel'
    people: 'FullPeople'
