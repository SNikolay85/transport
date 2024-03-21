from typing import Annotated

from fastapi import APIRouter, Depends

from trips.schema import PointAdd, RouteAdd, FuelAdd, CarAdd, CarFuelAdd, PositionAdd
from trips.schema import WhereDriveAdd, PeopleAdd, DriverAdd, PassengerAdd
from trips.reposit import DataLoads, DataGet


router = APIRouter(
    prefix='/routes',
    tags=['Trips']
)


@router.post('/point')
async def add_point(data: Annotated[PointAdd, Depends()]):
    point_data = await DataLoads.add_point(data)
    return point_data


@router.get('/point')
async def get_point():
    points = await DataGet.find_all_point()
    return {'points': points}


@router.post('/route')
async def add_route(route: Annotated[RouteAdd, Depends()]):
    route_data = await DataLoads.add_route(route)
    return route_data


@router.get('/route')
async def get_route():
    routes = await DataGet.find_all_route()
    return {'routes': routes}


@router.post('/fuel')
async def add_fuel(fuel: Annotated[FuelAdd, Depends()]):
    fuel_data = await DataLoads.add_fuel(fuel)
    return fuel_data


@router.get('/fuel')
async def get_fuel():
    fuels = await DataGet.find_all_fuel()
    return {'fuels': fuels}


@router.post('/car')
async def add_car(car: Annotated[CarAdd, Depends()]):
    car_data = await DataLoads.add_car(car)
    return car_data


@router.get('/car')
async def get_car():
    cars = await DataGet.find_all_car()
    return {'cars': cars}


@router.post('/car_fuel')
async def add_car_fuel(car_fuel: Annotated[CarFuelAdd, Depends()]):
    car_fuel_data = await DataLoads.add_car_fuel(car_fuel)
    return car_fuel_data


@router.get('/car_fuel')
async def get_car_fuel():
    car_fuels = await DataGet.find_all_car_fuel()
    return {'car_fuels': car_fuels}


@router.post('/position')
async def add_position(position: Annotated[PositionAdd, Depends()]):
    position_data = await DataLoads.add_position(position)
    return position_data


@router.get('/position')
async def get_position():
    positions = await DataGet.find_all_position()
    return {'positions': positions}


@router.post('/wd')
async def add_wd(wd: Annotated[WhereDriveAdd, Depends()]):
    wd_data = await DataLoads.add_wd(wd)
    return wd_data


@router.get('/wd')
async def get_wd():
    wd = await DataGet.find_all_wd()
    return {'wd': wd}


@router.post('/people')
async def add_people(people: Annotated[PeopleAdd, Depends()]):
    people_data = await DataLoads.add_people(people)
    return people_data


@router.get('/people')
async def get_people():
    peoples = await DataGet.find_all_people()
    return {'peoples': peoples}


@router.get('/people/{user_id}')
async def get_user(user_id: int):
    user = await DataGet.find_user(user_id)
    return {'user': user}


@router.post('/driver')
async def add_driver(driver: Annotated[DriverAdd, Depends()]):
    driver_data = await DataLoads.add_driver(driver)
    return driver_data


@router.get('/driver')
async def get_driver():
    drivers = await DataGet.find_all_driver()
    return {'drivers': drivers}


@router.post('/passenger')
async def add_passenger(passenger: Annotated[PassengerAdd, Depends()]):
    passenger_data = await DataLoads.add_passenger(passenger)
    return passenger_data


@router.get('/passenger')
async def get_passenger():
    passengers = await DataGet.find_all_passengers()
    return {'passengers': passengers}
