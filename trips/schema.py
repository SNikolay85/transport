from datetime import date
from typing import Optional

from pydantic import BaseModel

from trips.models import Fuel, WhereDrive


# --------------------------
# schemes for model Point
class PointAdd(BaseModel):
    name_point: str
    cost: int

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
# schemes for model CarFuel
class CarFuelAdd(BaseModel):
    id_car: int
    fuel: Fuel

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
    where_drive: WhereDrive

class FullPassenger(PassengerAdd):
    id_passenger: int

class FullPassengerRe(FullPassenger):
    people: 'FullPeople'
    driver: 'FullDriverRe'

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