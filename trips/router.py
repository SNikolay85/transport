import http
import time
from datetime import datetime, date
from typing import Annotated

from fastapi import APIRouter, Depends, Form, Body, HTTPException
from fastapi_cache.decorator import cache

from trips.schema import PointAdd, RouteAdd, FuelAdd, CarAdd, CarFuelAdd, PositionAdd, OrganizationAdd, RoleAdd
from trips.schema import WhereDriveAdd, PeopleAdd, DriverAdd, PassengerAdd, RefuelingAdd, OtherRouteAdd
from trips.schema import IdentificationAdd, PointPeopleAdd, PointOrganizationAdd
from trips.schema import OrganizationUpdate, PointUpdate, RouteUpdate, FuelUpdate, WhereDriveUpdate, PeopleUpdate
from trips.schema import CarUpdate, PositionUpdate, CarFuelUpdate, DriverUpdate, PassengerUpdate, OtherRouteUpdate
from trips.schema import IdentificationUpdate, RoleUpdate, DriverDate, PointPeopleUpdate, PointOrganizationUpdate

from trips.reposit import DataLoads, DataGet, UtilityFunction, DataPatch, Delete


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
router_identification = APIRouter(prefix='/identification', tags=['Identification'])
router_role = APIRouter(prefix='/role', tags=['Role'])
router_point_people = APIRouter(prefix='/point_people', tags=['PointPeople'])
router_point_organization = APIRouter(prefix='/point_organization', tags=['PointOrganization'])


# @router_point.post('/')
# async def add_point(data: PointAdd = Body()):
#     point_data = await DataLoads.add_point(data)
#     return {"message": f"{point_data['name_point']}, добавлено в базу"}
@router_point.post('/')
async def add_point(data: Annotated[PointAdd, Depends()]):
    if await UtilityFunction.check_name_point(data.name_point):
        raise HTTPException(status_code=422, detail='Такое название уже есть в базе')
    point_data = await DataLoads.add_point(data)
    return {"message": f"{point_data['name_point']}, добавлено в базу"}


@router_point.patch('/{id_point}')
async def change_point(id_point: int, point: Annotated[PointUpdate, Depends()]):
    if point.model_dump(exclude_none=True) == {}:
        raise HTTPException(status_code=422, detail='Для изменения нужно указать хотябы один параметр')
    point_data = await DataPatch.update_point(id_point, point)
    return point_data


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


# @router_point.get('/{name_point}')
# async def get_point(name_point:str):
#     points = await DataGet.find_name_point(name_point)
#     return points


@router_point.get('/')
async def get_point():
    points = await DataGet.find_all_point()
    return points


@router_point.delete('/{id_point}')
async def del_position(id_point: int):
    point = await Delete.del_point(id_point)
    if type(point) is str:
        return point
    else:
        return {'message': f'{point.name_point} удалено'}


@router_route.post('/')
async def add_route(route: Annotated[RouteAdd, Depends()]):
    name_route = await UtilityFunction.get_name_point(route)
    if await UtilityFunction.check_double_route(route):
        route_data = await DataLoads.add_route(route)
        return {"message": f"Маршрут {name_route[0].name_point} - {name_route[1].name_point} c расстоянием {route_data['distance']}, добавлено в базу"}
    else:
        return {
            "message": f"Маршрут {name_route[0].name_point} - {name_route[1].name_point} уже есть в базе"}


@router_route.patch('/{id_route}')
async def change_route(id_route: int, route: Annotated[RouteUpdate, Depends()]):
    if route.model_dump(exclude_none=True) == {}:
        raise HTTPException(status_code=422, detail='Для изменения нужно указать хотябы один параметр')
    route_data = await DataPatch.update_route(id_route, route)
    return route_data


@router_route.get('/')
async def get_route():
    routes = await DataGet.find_all_route()
    return {'routes': routes}


@router_route.delete('/{id_route}')
async def del_position(id_route: int):
    route = await Delete.del_route(id_route)
    if type(route) is str:
        return route
    else:
        return {'message': f'{route.id_start_point} - {route.id_finish_point} удалено'}


@router_fuel.post('/')
async def add_fuel(fuel: Annotated[FuelAdd, Depends()]):
    fuel_data = await DataLoads.add_fuel(fuel)
    return {"message": f"{fuel_data['name_fuel']}, добавлено в базу"}


@router_fuel.patch('/{id_fuel}')
async def change_fuel(id_fuel: int, fuel: Annotated[FuelUpdate, Depends()]):
    if fuel.model_dump(exclude_none=True) == {}:
        raise HTTPException(status_code=422, detail='Для изменения нужно указать хотябы один параметр')
    fuel_data = await DataPatch.update_fuel(id_fuel, fuel)
    return fuel_data


@router_fuel.get('/')
async def get_fuel():
    fuels = await DataGet.find_all_fuel()
    return {'fuels': fuels}


@router_fuel.delete('/{id_fuel}')
async def del_fuel(id_fuel: int):
    fuel = await Delete.del_fuel(id_fuel)
    if type(fuel) is str:
        return fuel
    else:
        return {'message': f'{fuel.name_fuel} удалено'}


@router_car.post('/')
async def add_car(car: Annotated[CarAdd, Depends()]):
    car_data = await DataLoads.add_car(car)
    return {"message": f"{car_data['name_car']}, добавлено в базу"}


@router_car.patch('/{id_car}')
async def change_car(id_car: int, car: Annotated[CarUpdate, Depends()]):
    if car.model_dump(exclude_none=True) == {}:
        raise HTTPException(status_code=422, detail='Для изменения нужно указать хотябы один параметр')
    car_data = await DataPatch.update_car(id_car, car)
    return car_data


@router_car.get('/')
async def get_car():
    cars = await DataGet.find_all_car()
    return {'cars': cars}


@router_car.delete('/{id_car}')
async def del_car(id_car: int):
    car = await Delete.del_car(id_car)
    if type(car) is str:
        return car
    else:
        return {'message': f'{car.name_car} удалено'}


@router_car_fuel.post('/')
async def add_car_fuel(car_fuel: Annotated[CarFuelAdd, Depends()]):
    car_fuel_data = await DataLoads.add_car_fuel(car_fuel)
    return car_fuel_data


@router_car_fuel.get('/')
async def get_car_fuel():
    car_fuels = await DataGet.find_all_car_fuel()
    return {'car_fuels': car_fuels}


@router_car_fuel.patch('/{id_car_fuel}')
async def change_car_fuel(id_car_fuel: int, car_fuel: Annotated[CarFuelUpdate, Depends()]):
    if car_fuel.model_dump(exclude_none=True) == {}:
        raise HTTPException(status_code=422, detail='Для изменения нужно указать хотябы один параметр')
    car_fuel_data = await DataPatch.update_car_fuel(id_car_fuel, car_fuel)
    return car_fuel_data


@router_car_fuel.delete('/{id_car_fuel}')
async def del_car_fuel(id_car_fuel: int):
    car_fuel = await Delete.del_car_fuel(id_car_fuel)
    if type(car_fuel) is str:
        return car_fuel
    else:
        return {'message': f'{car_fuel.id_car} - {car_fuel.id_fuel} удалено'}


@router_position.post('/')
async def add_position(position: Annotated[PositionAdd, Depends()]):
    position_data = await DataLoads.add_position(position)
    return position_data


@router_position.patch('/{id_position}')
async def change_position(id_position: int, position: Annotated[PositionUpdate, Depends()]):
    if position.model_dump(exclude_none=True) == {}:
        raise HTTPException(status_code=422, detail='Для изменения нужно указать хотябы один параметр')
    position_data = await DataPatch.update_position(id_position, position)
    return position_data


@router_position.get('/')
async def get_position():
    positions = await DataGet.find_all_position()
    return {'positions': positions}


@router_position.delete('/{id_position}')
async def del_position(id_position: int):
    position = await Delete.del_position(id_position)
    if type(position) is str:
        return position
    else:
        return {'message': f'{position.name_position} удалено'}


@router_wd.post('/')
async def add_wd(wd: Annotated[WhereDriveAdd, Depends()]):
    wd_data = await DataLoads.add_wd(wd)
    return {"message": f"{wd_data['name_wd']}, добавлено в базу"}


@router_wd.patch('/{id_wd}')
async def change_wd(id_wd: int, wd: Annotated[WhereDriveUpdate, Depends()]):
    if wd.model_dump(exclude_none=True) == {}:
        raise HTTPException(status_code=422, detail='Для изменения нужно указать хотябы один параметр')
    wd_data = await DataPatch.update_wd(id_wd, wd)
    return wd_data


@router_wd.get('/')
async def get_wd():
    wd = await DataGet.find_all_wd()
    return {'where_drive': wd}


@router_wd.delete('/{id_wd}')
async def del_wd(id_wd: int):
    wd = await Delete.del_wd(id_wd)
    if type(wd) is str:
        return wd
    else:
        return {'message': f'{wd.name_wd} удалено'}


@router_people.post('/')
async def add_people(people: Annotated[PeopleAdd, Depends()]):
    people_data = await DataLoads.add_people(people)
    return people_data


@router_people.patch('/{id_people}')
async def change_people(id_people: int, people: Annotated[PeopleUpdate, Depends()]):
    if people.model_dump(exclude_none=True) == {}:
        raise HTTPException(status_code=422, detail='Для изменения нужно указать хотябы один параметр')
    people_data = await DataPatch.update_people(id_people, people)
    return people_data


@router_people.get('/')
async def get_people():
    peoples = await DataGet.find_all_people()
    return {'peoples': peoples}


@router_people.delete('/{id_people}')
async def del_people(id_people: int):
    people = await Delete.del_people(id_people)
    if type(people) is str:
        return people
    else:
        return {'message': f'{people.last_name} {people.first_name} удален'}


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
    organization_data = await DataPatch.update_organization(id_organization, organization)
    return organization_data


@router_organization.get('/')
async def get_organization():
    organizations = await DataGet.find_all_organization()
    return {'organizations': organizations}


@router_organization.delete('/{id_organization}')
async def del_organization(id_organization: int):
    organization = await Delete.del_organization(id_organization)
    if type(organization) is str:
        return organization
    else:
        return {'message': f'{organization.name_organization} удалено'}


@router_driver.post('/')
async def add_driver(driver: Annotated[DriverAdd, Depends()]):
    check_address = await UtilityFunction.check_people_address(driver)
    if check_address is None:
        raise HTTPException(status_code=422, detail='Неверно указан адрес водителя')
    driver_data = await DataLoads.add_driver(driver)
    return driver_data


@router_driver.patch('/{id_driver}')
async def change_driver(id_driver: int, driver: Annotated[DriverUpdate, Depends()]):
    if driver.model_dump(exclude_none=True) == {}:
        raise HTTPException(status_code=422, detail='Для изменения нужно указать хотябы один параметр')
    current_driver = await DataGet.find_driver(id_driver)
    if driver.id_people and driver.id_point is None:
        driver.id_point = current_driver.id_point
    elif driver.id_point and driver.id_people is None:
        driver.id_people = current_driver.id_people
    check_address = await UtilityFunction.check_people_address(driver)
    if check_address is None:
        raise HTTPException(status_code=422, detail='Неверно указан адрес водителя')
    driver_data = await DataPatch.update_driver(id_driver, driver)
    return driver_data


@router_driver.get('/')
async def get_driver():
    car_carrier = await DataGet.find_all_car_carrier()
    return {'car_carrier': car_carrier}


@router_driver.delete('/{id_driver}')
async def del_driver(id_driver: int):
    driver = await Delete.del_driver(id_driver)
    if type(driver) is str:
        return driver
    else:
        return {'message': f'{driver.id_people} удалено'}


@router_driver.get('/{now_date_trip}')
async def get_date_trip_driver(now_date_trip: datetime):
    car_carrier = await DataGet.find_driver_of_date(now_date_trip)
    return {'car_carrier': car_carrier}


@router_driver.get('/distance/{id_driver}')
async def get_distance_of_driver(id_driver: int):
    dist_driver = await UtilityFunction.find_distance_of_driver(id_driver)
    return {'passenger_of_driver': dist_driver[0],
            'organization_of_driver': dist_driver[1],
            'distance_forward': dist_driver[2],
            'route_of_point_f': dist_driver[3],
            'distance_aw': dist_driver[4],
            'route_of_point_aw': dist_driver[5]
            }


@router_driver.get('/balance/{id_people}/{month_trips}')
@cache(expire=30)
async def get_balance(id_people: int, month_trip: Annotated[DriverDate, Depends()]):
    balance = await UtilityFunction.get_count_gas(id_people, month_trip)
    return balance


@router_passenger.post('/')
async def add_passenger(passenger: Annotated[PassengerAdd, Depends()]):
    check_address = await UtilityFunction.check_people_address(passenger)
    if check_address is None:
        raise HTTPException(status_code=422, detail='Неверно указан адрес пассажира')
    passenger_data = await DataLoads.add_passenger(passenger)
    return passenger_data


@router_passenger.patch('/{id_passenger}')
async def change_passenger(id_passenger: int, passenger: Annotated[PassengerUpdate, Depends()]):
    if passenger.model_dump(exclude_none=True) == {}:
        raise HTTPException(status_code=422, detail='Для изменения нужно указать хотябы один параметр')
    current_passenger = await DataGet.find_passenger(id_passenger)
    if passenger.id_people and passenger.id_point is None:
        passenger.id_point = current_passenger.id_point
    elif passenger.id_point and passenger.id_people is None:
        passenger.id_people = current_passenger.id_people
    check_address = await UtilityFunction.check_people_address(passenger)
    if check_address is None:
        raise HTTPException(status_code=422, detail='Неверно указан адрес пассажира')
    passenger_data = await DataPatch.update_passenger(id_passenger, passenger)
    return passenger_data


@router_passenger.get('/')
async def get_passenger():
    passengers = await DataGet.find_all_passengers()
    return {'passengers': passengers}


@router_passenger.delete('/{id_passenger}')
async def del_passenger(id_passenger: int):
    passenger = await Delete.del_passenger(id_passenger)
    if type(passenger) is str:
        return passenger
    else:
        return {'message': f'{passenger.id_people} удалено'}


@router_other_route.post('/')
async def add_other_route(other_route: Annotated[OtherRouteAdd, Depends()]):
    check_address = await UtilityFunction.check_organization_address(other_route)
    if check_address is None:
        raise HTTPException(status_code=422, detail='Неверно указан адрес организации')
    other_route_data = await DataLoads.add_other_route(other_route)
    return other_route_data


@router_other_route.patch('/{id_other_route}')
async def change_other_route(id_other_route: int, other_route: Annotated[OtherRouteUpdate, Depends()]):
    if other_route.model_dump(exclude_none=True) == {}:
        raise HTTPException(status_code=422, detail='Для изменения нужно указать хотябы один параметр')
    current_other_route = await DataGet.find_other_route(id_other_route)
    if other_route.id_organization and other_route.id_point is None:
        other_route.id_point = current_other_route.id_point
    elif other_route.id_point and other_route.id_organization is None:
        other_route.id_organization = current_other_route.id_organization
    check_address = await UtilityFunction.check_organization_address(other_route)
    if check_address is None:
        raise HTTPException(status_code=422, detail='Неверно указан адрес организации')
    other_route_data = await DataPatch.update_other_route(id_other_route, other_route)
    return other_route_data


@router_other_route.get('/')
async def get_other_route():
    other_routes = await DataGet.find_all_other_route()
    return {'other_routes': other_routes}


@router_other_route.delete('/{id_other_route}')
async def del_other_route(id_other_route: int):
    other_route = await Delete.del_other_route(id_other_route)
    if type(other_route) is str:
        return other_route
    else:
        return {'message': f'{other_route.id_organization} удалено'}


@router_refueling.post('/')
async def add_refueling(refueling: Annotated[RefuelingAdd, Depends()]):
    refueling_data = await DataLoads.add_refueling(refueling)
    return refueling_data


@router_refueling.post('/auto/')
async def add_refueling_auto():
    refueling_data = await DataLoads.add_refueling_auto()
    return refueling_data


@router_refueling.get('/')
async def get_refueling():
    refuelings = await DataGet.find_all_refuelings()
    return {'refuelings': refuelings}


@router_refueling.delete('/{id_refueling}')
async def del_refueling(id_refueling: int):
    refueling = await Delete.del_refueling(id_refueling)
    if type(refueling) is str:
        return refueling
    else:
        return {'message': f'{refueling.date_refueling} - {refueling.quantity} удалено'}


@router_refueling.get('/count/{date_start}/{date_finish}')
async def get_refueling(date_start, date_finish):
    count_refueling = await DataGet.count_refueling_to_date(date_start, date_finish)
    return {'refuelings': count_refueling}


@router_identification.post('/')
async def add_identification(identification: Annotated[IdentificationAdd, Depends()]):
    identification_data = await DataLoads.add_identification(identification)
    return {"message": f"{identification_data['id_tg']}, добавлено в базу"}


@router_identification.patch('/{id_identification}')
async def change_identification(id_identification: int, identification: Annotated[IdentificationUpdate, Depends()]):
    if identification.model_dump(exclude_none=True) == {}:
        raise HTTPException(status_code=422, detail='Для изменения нужно указать хотябы один параметр')
    identification_data = await DataPatch.update_identification(id_identification, identification)
    return identification_data


@router_identification.get('/')
async def get_identification():
    identifications = await DataGet.find_all_identification()
    return {'identifications': identifications}


@router_identification.delete('/{id_identification}')
async def del_identification(id_identification: int):
    identification = await Delete.del_identification(id_identification)
    if type(identification) is str:
        return identification
    else:
        return {'message': f'{identification.id_tg} удалено'}


@router_role.post('/')
async def add_role(role: Annotated[RoleAdd, Depends()]):
    role_data = await DataLoads.add_role(role)
    return {"message": f"{role_data['name_role']}, добавлено в базу"}


@router_role.patch('/{id_role}')
async def change_role(id_role: int, role: Annotated[RoleUpdate, Depends()]):
    if role.model_dump(exclude_none=True) == {}:
        raise HTTPException(status_code=422, detail='Для изменения нужно указать хотябы один параметр')
    role_data = await DataPatch.update_role(id_role, role)
    return role_data


@router_role.get('/')
async def get_role():
    roles = await DataGet.find_all_role()
    return {'roles': roles}


@router_role.delete('/{id_role}')
async def del_role(id_role: int):
    role = await Delete.del_role(id_role)
    if type(role) is str:
        return role
    else:
        return {'message': f'{role.name_role} удалено'}


@router_point_people.post('/')
async def add_point_people(point_people: Annotated[PointPeopleAdd, Depends()]):
    point_people_data = await DataLoads.add_point_people(point_people)
    return point_people_data


@router_point_people.get('/')
async def get_point_people():
    point_peoples = await DataGet.find_all_point_people()
    return {'point_peoples': point_peoples}


@router_point_people.patch('/{id_point_people}')
async def change_point_people(id_point_people: int, point_people: Annotated[PointPeopleUpdate, Depends()]):
    if point_people.model_dump(exclude_none=True) == {}:
        raise HTTPException(status_code=422, detail='Для изменения нужно указать хотябы один параметр')
    point_people_data = await DataPatch.update_point_people(id_point_people, point_people)
    return point_people_data


@router_point_people.delete('/{id_point_people}')
async def del_point_people(id_point_people: int):
    point_people = await Delete.del_point_people(id_point_people)
    if type(point_people) is str:
        return point_people
    else:
        return {'message': f'{point_people.id_point} - {point_people.id_people} удалено'}


@router_point_organization.post('/')
async def add_point_organization(point_organization: Annotated[PointOrganizationAdd, Depends()]):
    point_organization_data = await DataLoads.add_point_organization(point_organization)
    return point_organization_data


@router_point_organization.get('/')
async def get_point_organization():
    point_organizations = await DataGet.find_all_point_organization()
    return {'point_organizations': point_organizations}


@router_point_organization.patch('/{id_point_organization}')
async def change_point_organization(id_point_organization: int, point_organization: Annotated[PointOrganizationUpdate, Depends()]):
    if point_organization.model_dump(exclude_none=True) == {}:
        raise HTTPException(status_code=422, detail='Для изменения нужно указать хотябы один параметр')
    point_organization_data = await DataPatch.update_point_organization(id_point_organization, point_organization)
    return point_organization_data


@router_point_organization.delete('/{id_point_organization}')
async def del_point_organization(id_point_organization: int):
    point_organization = await Delete.del_point_organization(id_point_organization)
    if type(point_organization) is str:
        return point_organization
    else:
        return {'message': f'{point_organization.id_point} - {point_organization.id_organization} удалено'}
