import time
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Form, Body, HTTPException
from fastapi_cache.decorator import cache

from trips.schema import PointAdd, RouteAdd, FuelAdd, CarAdd, CarFuelAdd, PositionAdd, OrganizationAdd
from trips.schema import WhereDriveAdd, PeopleAdd, DriverAdd, PassengerAdd, RefuelingAdd, OtherRouteAdd
from trips.schema import OrganizationUpdate

from trips.reposit import DataLoads, DataGet, UtilityFunction, DataPut

router_point = APIRouter(prefix='/point', tags=['Point'])
router_route = APIRouter(prefix='/route', tags=['Route'])
router_fuel = APIRouter(prefix='/fuel', tags=['Fuel'])
router_car = APIRouter(prefix='/car', tags=['Car'])
router_car_fuel = APIRouter(prefix='/car_fuel', tags=['CarFuel'])
router_position = APIRouter(prefix='/position', tags=['Position'])
router_wd = APIRouter(prefix='/wd', tags=['WhereDrive'])
router_people = APIRouter(prefix='/people', tags=['People'])
router_organization = APIRouter(prefix='/organization', tags=['Organization'])
router_driver = APIRouter(prefix='/driver', tags=['Driver'])
router_passenger = APIRouter(prefix='/passenger', tags=['Passenger'])
router_other_route = APIRouter(prefix='/other_route', tags=['OtherRoute'])
router_refueling = APIRouter(prefix='/refueling', tags=['Refueling'])


# @router_point.post('/')
# async def add_point(data: PointAdd = Body()):
#     point_data = await DataLoads.add_point(data)
#     return {"message": f"{point_data['name_point']}, добавлено в базу"}
@router_point.post('/')
async def add_point(data: Annotated[PointAdd, Depends()]):
    point_data = await DataLoads.add_point(data)
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


@router_route.post('/')
async def add_route(route: Annotated[RouteAdd, Depends()]):
    name_route = await UtilityFunction.get_name_point(route)
    if await UtilityFunction.check_double_route(route):
        route_data = await DataLoads.add_route(route)
        return {"message": f"Маршрут {name_route[0].name_point} - {name_route[1].name_point} c расстоянием {route_data['distance']}, добавлено в базу"}
    else:
        return {
            "message": f"Маршрут {name_route[0].name_point} - {name_route[1].name_point} уже есть в базе"}


@router_route.get('/')
async def get_route():
    routes = await DataGet.find_all_route()
    return {'routes': routes}


@router_fuel.post('/')
async def add_fuel(fuel: Annotated[FuelAdd, Depends()]):
    fuel_data = await DataLoads.add_fuel(fuel)
    return {"message": f"{fuel_data['name_fuel']}, добавлено в базу"}


@router_fuel.get('/')
async def get_fuel():
    fuels = await DataGet.find_all_fuel()
    return {'fuels': fuels}


@router_car.post('/')
async def add_car(car: Annotated[CarAdd, Depends()]):
    car_data = await DataLoads.add_car(car)
    return {"message": f"{car_data['name_car']}, добавлено в базу"}


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


@router_wd.post('/')
async def add_wd(wd: Annotated[WhereDriveAdd, Depends()]):
    wd_data = await DataLoads.add_wd(wd)
    return {"message": f"{wd_data['name_wd']}, добавлено в базу"}


@router_wd.get('/')
async def get_wd():
    wd = await DataGet.find_all_wd()
    return {'where_drive': wd}


@router_people.post('/')
async def add_people(people: Annotated[PeopleAdd, Depends()]):
    people_data = await DataLoads.add_people(people)
    return people_data


@router_people.get('/')
async def get_people():
    peoples = await DataGet.find_all_people()
    return {'peoples': peoples}


@router_people.get('/driver/')
async def get_people():
    drivers = await DataGet.find_all_driver()
    return {'drivers': drivers}


@router_people.get('/{user_id}')
async def get_user(user_id: int):
    user = await DataGet.find_user(user_id)
    return {'user': user}

@router_organization.post('/')
async def add_organization(organization: Annotated[OrganizationAdd, Depends()]):
    organization_data = await DataLoads.add_organization(organization)
    return organization_data


@router_organization.patch('/{id_organization}')
async def change_organization(id_organization: int, organization: Annotated[OrganizationUpdate, Depends()]):
    if organization.model_dump(exclude_none=True) == {}:
        raise HTTPException(status_code=422, detail='Для изменения нужно указать хотябы один параметр')
    organization_data = await DataPut.update_organization(id_organization, organization)
    return organization_data


@router_organization.get('/')
async def get_organization():
    organizations = await DataGet.find_all_organization()
    return {'organizations': organizations}


@router_driver.post('/')
async def add_driver(driver: Annotated[DriverAdd, Depends()]):
    driver_data = await DataLoads.add_driver(driver)
    return driver_data


@router_driver.get('/')
async def get_driver():
    car_carrier = await DataGet.find_all_car_carrier()
    return {'car_carrier': car_carrier}


@router_driver.get('/{now_date_trip}')
async def get_date_trip_driver(now_date_trip: datetime):
    car_carrier = await DataGet.find_driver_of_date(now_date_trip)
    return {'car_carrier': car_carrier}


@router_passenger.post('/')
async def add_passenger(passenger: Annotated[PassengerAdd, Depends()]):
    passenger_data = await DataLoads.add_passenger(passenger)
    return passenger_data


@router_passenger.get('/')
async def get_passenger():
    passengers = await DataGet.find_all_passengers()
    return {'passengers': passengers}

@router_passenger.get('/{id_driver}')
async def get_passenger_of_driver(id_driver: int):
    pas_driver = await DataGet.find_passenger_of_driver(id_driver)
    return {'passenger_of_driver': pas_driver[0],
            'distance_forward': pas_driver[1],
            'route_of_point_f': pas_driver[2],
            'distance_aw': pas_driver[3],
            'route_of_point_aw': pas_driver[4]
            }

@router_other_route.post('/')
async def add_other_route(other_route: Annotated[OtherRouteAdd, Depends()]):
    other_route_data = await DataLoads.add_other_route(other_route)
    return other_route_data


@router_other_route.get('/')
async def get_other_route():
    other_routes = await DataGet.find_all_other_route()
    return {'other_routes': other_routes}

@router_refueling.post('/')
async def add_refueling(refueling: Annotated[RefuelingAdd, Depends()]):
    refueling_data = await DataLoads.add_refueling(refueling)
    return refueling_data


@router_refueling.get('/')
async def get_refueling():
    refuelings = await DataGet.find_all_refuelings()
    return {'refuelings': refuelings}

