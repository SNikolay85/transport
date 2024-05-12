from typing import Annotated

from fastapi import APIRouter, Depends

from trips.schema import PointAdd, RouteAdd, CarAdd, CarFuelAdd, PositionAdd, PeopleAdd, DriverAdd, PassengerAdd

from trips.reposit import DataLoads, DataGet


router_point = APIRouter(prefix='/point', tags=['Point'])
router_route = APIRouter(prefix='/route', tags=['Route'])
router_car = APIRouter(prefix='/car', tags=['Car'])
router_car_fuel = APIRouter(prefix='/car_fuel', tags=['CarFuel'])
router_position = APIRouter(prefix='/position', tags=['Position'])
router_people = APIRouter(prefix='/people', tags=['People'])
router_driver = APIRouter(prefix='/driver', tags=['Driver'])
router_passenger = APIRouter(prefix='/passenger', tags=['Passenger'])


@router_point.post('/')
async def add_point(data: Annotated[PointAdd, Depends()]):
    point_data = await DataLoads.add_point(data)
    return point_data


@router_point.get('/all_name_point/', response_model=dict)
async def get_point():
    points = await DataGet.all_name_point()
    return points

@router_point.get('/{name_point}')
async def get_point(name_point:str):
    points = await DataGet.find_name_point(name_point)
    return points

@router_point.get('/all_point/')
async def get_point():
    points = await DataGet.find_all_point()
    return points


@router_route.post('/')
async def add_route(route: Annotated[RouteAdd, Depends()]):
    route_data = await DataLoads.add_route(route)
    return route_data


@router_route.get('/')
async def get_route():
    routes = await DataGet.find_all_route()
    return {'routes': routes}


@router_car.post('/')
async def add_car(car: Annotated[CarAdd, Depends()]):
    car_data = await DataLoads.add_car(car)
    return car_data


@router_car.get('/')
async def get_car():
    cars = await DataGet.find_all_car()
    return {'cars': cars}


@router_car_fuel.post('/')
async def add_car_fuel(car_fuel: Annotated[CarFuelAdd, Depends()]):
    car_fuel_data = await DataLoads.add_car_fuel(car_fuel)
    return car_fuel_data


@router_car_fuel.get('/')
async def get_car_fuel():
    car_fuels = await DataGet.find_all_car_fuel()
    return {'car_fuels': car_fuels}


@router_position.post('/')
async def add_position(position: Annotated[PositionAdd, Depends()]):
    position_data = await DataLoads.add_position(position)
    return position_data


@router_position.get('/')
async def get_position():
    positions = await DataGet.find_all_position()
    return {'positions': positions}


@router_people.post('/')
async def add_people(people: Annotated[PeopleAdd, Depends()]):
    people_data = await DataLoads.add_people(people)
    return people_data


@router_people.get('/')
async def get_people():
    peoples = await DataGet.find_all_people()
    return {'peoples': peoples}


@router_people.get('/{user_id}')
async def get_user(user_id: int):
    user = await DataGet.find_user(user_id)
    return {'user': user}


@router_driver.post('/')
async def add_driver(driver: Annotated[DriverAdd, Depends()]):
    driver_data = await DataLoads.add_driver(driver)
    return driver_data


@router_driver.get('/')
async def get_driver():
    drivers = await DataGet.find_all_driver()
    return {'drivers': drivers}


@router_passenger.post('/')
async def add_passenger(passenger: Annotated[PassengerAdd, Depends()]):
    passenger_data = await DataLoads.add_passenger(passenger)
    return passenger_data


@router_passenger.get('/')
async def get_passenger():
    passengers = await DataGet.find_all_passengers()
    return {'passengers': passengers}
