from datetime import date
from typing import Optional

from pydantic import BaseModel, Field

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
    name_point: str = Field(max_lenght=100)
    cost: int = Field(ge=0)

class FullPoint(PointAdd):
    id_point: int

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

# --------------------------
# schemes for model WhereDrive
class WhereDriveAdd(BaseModel):
    name_wd: str

class FullWhereDrive(WhereDriveAdd):
    id_wd: int

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
    driving_licence: Optional[str]

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

class FullDriver(DriverAdd):
    id_driver: int

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

class FullPassengerRe(FullPassenger):
    people: 'FullPeople'
    driver: 'FullDriverRe'
    wd: 'FullWhereDrive'

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
    distance: int

class FullRoute(RouteAdd):
    id_route: int

class FullRouteRe(FullRoute):
    point_start: 'FullPoint'
    point_finish: 'FullPoint'

# --------------------------
# schemes for model Refueling
class RefuelingAdd(BaseModel):
    id_fuel: int
    id_people: int
    date_refueling: date

class FullRefueling(RefuelingAdd):
    id_refueling: int