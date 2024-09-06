import time
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Form, Body
from fastapi_cache.decorator import cache

from trips.schema import PointAdd, RouteAdd, FuelAdd, CarAdd, CarFuelAdd, PositionAdd
from trips.schema import WhereDriveAdd, PeopleAdd, DriverAdd, PassengerAdd, RefuelingAdd

from trips.reposit import DataLoads, DataGet, RealDataLoads, RealDataGet

router_point = APIRouter(prefix='/point', tags=['Point'])
router_route = APIRouter(prefix='/route', tags=['Route'])
router_fuel = APIRouter(prefix='/fuel', tags=['Fuel'])
router_car = APIRouter(prefix='/car', tags=['Car'])
router_car_fuel = APIRouter(prefix='/car_fuel', tags=['CarFuel'])
router_position = APIRouter(prefix='/position', tags=['Position'])
router_wd = APIRouter(prefix='/wd', tags=['WhereDrive'])
router_people = APIRouter(prefix='/people', tags=['People'])
router_driver = APIRouter(prefix='/driver', tags=['Driver'])
router_passenger = APIRouter(prefix='/passenger', tags=['Passenger'])
router_refueling = APIRouter(prefix='/refueling', tags=['Refueling'])


# @router_point.post('/')
# async def add_point(data: PointAdd = Body()):
#     point_data = await DataLoads.add_point(data)
#     return {"message": f"{point_data['name_point']}, добавлено в базу"}
@router_point.post('/')
async def add_point(data: Annotated[PointAdd, Depends()]):
    point_data = await DataLoads.add_point(data)
    return {"message": f"{point_data['name_point']}, добавлено в базу"}

@router_point.post('/real/')
async def add_point(data: Annotated[PointAdd, Depends()]):
    point_data = await RealDataLoads.add_point(data)
    return {"message": f"{point_data['name_point']}, добавлено в базу"}

# @router_point.post('/')
# async def add_point(data: Annotated[PointAdd, Body(), Depends()]):
# #async def add_point(name_point: str=Form(), cost: int=Form()):
#     # data = {'name_point': name_point, 'cost': cost}
#     print(data)
#     point_data = await DataLoads.add_point(data)
#     return point_data


@router_point.get('/all_name_point/', response_model=dict)
@cache(expire=30)
async def get_point():
    time.sleep(2)
    points = await DataGet.all_name_point()
    return points


@router_point.get('/{name_point}')
async def get_point(name_point:str):
    points = await DataGet.find_name_point(name_point)
    return points


@router_point.get('/')
async def get_point():
    points = await DataGet.find_all_point()
    return points


@router_point.get('/real/')
async def get_point():
    points = await RealDataGet.find_all_point()
    return points


@router_route.post('/')
async def add_route(route: Annotated[RouteAdd, Depends()]):
    route_data = await DataLoads.add_route(route)
    return {"message": f"Маршрут {route_data['id_start_point']} - {route_data['id_finish_point']} c расстоянием {route_data['distance']}, добавлено в базу"}


@router_route.post('/real/')
async def add_route(route: Annotated[RouteAdd, Depends()]):
    route_data = await RealDataLoads.add_route(route)
    print(route_data)
    return {"message": f"Маршрут {route_data['id_start_point']} - {route_data['id_finish_point']} c расстоянием {route_data['distance']}, добавлено в базу"}


@router_route.get('/')
async def get_route():
    routes = await DataGet.find_all_route()
    return {'routes': routes}


@router_route.get('/real/')
async def get_route():
    routes = await RealDataGet.find_all_route()
    return {'routes': routes}


@router_fuel.post('/')
async def add_fuel(fuel: Annotated[FuelAdd, Depends()]):
    fuel_data = await DataLoads.add_fuel(fuel)
    return {"message": f"{fuel_data['name_fuel']}, добавлено в базу"}


@router_fuel.post('/real/')
async def add_fuel(fuel: Annotated[FuelAdd, Depends()]):
    fuel_data = await RealDataLoads.add_fuel(fuel)
    return {"message": f"{fuel_data['name_fuel']}, добавлено в базу"}


@router_fuel.get('/')
async def get_fuel():
    fuels = await DataGet.find_all_fuel()
    return {'fuels': fuels}


@router_fuel.get('/real/')
async def get_route():
    fuels = await RealDataGet.find_all_fuel()
    return {'fuels': fuels}

@router_car.post('/')
async def add_car(car: Annotated[CarAdd, Depends()]):
    car_data = await DataLoads.add_car(car)
    return {"message": f"{car_data['name_car']}, добавлено в базу"}


@router_car.post('/real/')
async def add_car(car: Annotated[CarAdd, Depends()]):
    car_data = await RealDataLoads.add_car(car)
    return {"message": f"{car_data['name_car']}, добавлено в базу"}


@router_car.get('/')
async def get_car():
    cars = await DataGet.find_all_car()
    return {'cars': cars}


@router_car.get('/real/')
async def get_car():
    cars = await RealDataGet.find_all_car()
    return {'cars': cars}


@router_car_fuel.post('/')
async def add_car_fuel(car_fuel: Annotated[CarFuelAdd, Depends()]):
    car_fuel_data = await DataLoads.add_car_fuel(car_fuel)
    return car_fuel_data


@router_car_fuel.post('/real/')
async def add_car_fuel(car_fuel: Annotated[CarFuelAdd, Depends()]):
    car_fuel_data = await RealDataLoads.add_car_fuel(car_fuel)
    return car_fuel_data


@router_car_fuel.get('/')
async def get_car_fuel():
    car_fuels = await DataGet.find_all_car_fuel()
    return {'car_fuels': car_fuels}


@router_car_fuel.get('/real/')
async def get_car_fuel():
    car_fuels = await RealDataGet.find_all_car_fuel()
    return {'car_fuels': car_fuels}


@router_position.post('/')
async def add_position(position: Annotated[PositionAdd, Depends()]):
    position_data = await DataLoads.add_position(position)
    return position_data


@router_position.post('/real/')
async def add_position(position: Annotated[PositionAdd, Depends()]):
    position_data = await RealDataLoads.add_position(position)
    return position_data


@router_position.get('/')
async def get_position():
    positions = await DataGet.find_all_position()
    return {'positions': positions}


@router_position.get('/real/')
async def get_position():
    positions = await RealDataGet.find_all_position()
    return {'positions': positions}


@router_wd.post('/')
async def add_wd(wd: Annotated[WhereDriveAdd, Depends()]):
    wd_data = await DataLoads.add_wd(wd)
    return {"message": f"{wd_data['name_wd']}, добавлено в базу"}


@router_wd.post('/real/')
async def add_wd(wd: Annotated[WhereDriveAdd, Depends()]):
    wd_data = await RealDataLoads.add_wd(wd)
    return {"message": f"{wd_data['name_wd']}, добавлено в базу"}


@router_wd.get('/')
async def get_wd():
    wd = await DataGet.find_all_wd()
    return {'where_drive': wd}


@router_wd.get('/real/')
async def get_wd():
    wd = await RealDataGet.find_all_wd()
    return {'where_drive': wd}


@router_people.post('/')
async def add_people(people: Annotated[PeopleAdd, Depends()]):
    people_data = await DataLoads.add_people(people)
    return people_data


@router_people.post('/real/')
async def add_people(people: Annotated[PeopleAdd, Depends()]):
    people_data = await RealDataLoads.add_people(people)
    return people_data


@router_people.get('/')
async def get_people():
    peoples = await DataGet.find_all_people()
    return {'peoples': peoples}


@router_people.get('/real/')
async def get_people():
    peoples = await RealDataGet.find_all_people()
    return {'peoples': peoples}


@router_people.get('/driver/')
async def get_people():
    drivers = await DataGet.find_all_driver()
    return {'drivers': drivers}


@router_people.get('/driver/real/')
async def get_people():
    drivers = await RealDataGet.find_all_driver()
    return {'drivers': drivers}


@router_people.get('/{user_id}')
async def get_user(user_id: int):
    user = await DataGet.find_user(user_id)
    return {'user': user}


@router_people.get('/real/{user_id}')
async def get_user(user_id: int):
    user = await RealDataGet.find_user(user_id)
    return {'user': user}


@router_driver.post('/')
async def add_driver(driver: Annotated[DriverAdd, Depends()]):
    driver_data = await DataLoads.add_driver(driver)
    return driver_data


@router_driver.post('/real/')
async def add_driver(driver: Annotated[DriverAdd, Depends()]):
    driver_data = await RealDataLoads.add_driver(driver)
    return driver_data


@router_driver.get('/')
async def get_driver():
    car_carrier = await DataGet.find_all_car_carrier()
    return {'car_carrier': car_carrier}


@router_driver.get('/real/')
async def get_driver():
    car_carrier = await RealDataGet.find_all_car_carrier()
    return {'car_carrier': car_carrier}


@router_driver.get('/{now_date_trip}')
async def get_date_trip_driver(now_date_trip: datetime):
    car_carrier = await DataGet.find_driver_of_date(now_date_trip)
    return {'car_carrier': car_carrier}


@router_driver.get('/real/{now_date_trip}')
async def get_date_trip_driver(now_date_trip: datetime):
    car_carrier = await RealDataGet.find_driver_of_date(now_date_trip)
    return {'car_carrier': car_carrier}


@router_passenger.post('/')
async def add_passenger(passenger: Annotated[PassengerAdd, Depends()]):
    passenger_data = await DataLoads.add_passenger(passenger)
    return passenger_data


@router_passenger.post('/real/')
async def add_passenger(passenger: Annotated[PassengerAdd, Depends()]):
    passenger_data = await RealDataLoads.add_passenger(passenger)
    return passenger_data


@router_passenger.get('/')
async def get_passenger():
    passengers = await DataGet.find_all_passengers()
    return {'passengers': passengers}


@router_passenger.get('/real/')
async def get_passenger():
    passengers = await RealDataGet.find_all_passengers()
    return {'passengers': passengers}


@router_refueling.post('/')
async def add_refueling(refueling: Annotated[RefuelingAdd, Depends()]):
    refueling_data = await DataLoads.add_refueling(refueling)
    return refueling_data


@router_refueling.post('/real/')
async def add_refueling(refueling: Annotated[RefuelingAdd, Depends()]):
    refueling_data = await RealDataLoads.add_refueling(refueling)
    return refueling_data


@router_refueling.get('/')
async def get_refueling():
    refuelings = await DataGet.find_all_refuelings()
    return {'refuelings': refuelings}


@router_refueling.get('/real/')
async def get_refueling():
    refuelings = await RealDataGet.find_all_refuelings()
    return {'refuelings': refuelings}
