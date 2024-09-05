from sqlalchemy import select
import asyncio
import os
import json

from trips.models import Session, Point, Route, Fuel, Car, CarFuel, Position
from trips.models import WhereDrive, People, Driver, Passenger, Refueling

from trips.schema import FullPoint, FullRoute, FullFuel, FullWhereDrive, FullPosition, FullPeople
from trips.schema import FullCar, FullCarFuel, FullDriver, FullPassenger, FullRefueling

current = os.getcwd()
file_name_base = '../download_data.json'
full_path = os.path.join(current, file_name_base)

async def download_all():
    all_data = []
    async with Session() as session:
        query_point = select(Point)
        result_point = await session.execute(query_point)
        point_models = result_point.unique().scalars().all()
        point_dto = [FullPoint.model_validate(row, from_attributes=True) for row in point_models]
        for i in point_dto:
            dict_temp = {'model': 'point', 'fields': {}}
            dict_temp['fields']['id_point'] = i.id_point
            dict_temp['fields']['name'] = i.name_point
            dict_temp['fields']['cost'] = i.cost
            all_data.append(dict_temp)

        query_route = select(Route)
        result_route = await session.execute(query_route)
        route_models = result_route.unique().scalars().all()
        route_dto = [FullRoute.model_validate(row, from_attributes=True) for row in route_models]
        for i in route_dto:
            dict_temp = {'model': 'route', 'fields': {}}
            dict_temp['fields']['id_route'] = i.id_route
            dict_temp['fields']['start'] = i.id_start_point
            dict_temp['fields']['finish'] = i.id_finish_point
            dict_temp['fields']['distance'] = i.distance
            all_data.append(dict_temp)

        query_fuel = select(Fuel)
        result_fuel = await session.execute(query_fuel)
        fuel_models = result_fuel.unique().scalars().all()
        fuel_dto = [FullFuel.model_validate(row, from_attributes=True) for row in fuel_models]
        for i in fuel_dto:
            dict_temp = {'model': 'fuel', 'fields': {}}
            dict_temp['fields']['id_fuel'] = i.id_fuel
            dict_temp['fields']['name'] = i.name_fuel
            all_data.append(dict_temp)

        query_wd = select(WhereDrive)
        result_wd = await session.execute(query_wd)
        wd_models = result_wd.unique().scalars().all()
        wd_dto = [FullWhereDrive.model_validate(row, from_attributes=True) for row in wd_models]
        for i in wd_dto:
            dict_temp = {'model': 'where_drive', 'fields': {}}
            dict_temp['fields']['id_wd'] = i.id_wd
            dict_temp['fields']['name'] = i.name_wd
            all_data.append(dict_temp)

        query_position = select(Position)
        result_position = await session.execute(query_position)
        position_models = result_position.unique().scalars().all()
        position_dto = [FullPosition.model_validate(row, from_attributes=True) for row in position_models]
        for i in position_dto:
            dict_temp = {'model': 'position', 'fields': {}}
            dict_temp['fields']['id_position'] = i.id_position
            dict_temp['fields']['name'] = i.name_position
            all_data.append(dict_temp)

        query_people = select(People)
        result_people = await session.execute(query_people)
        people_models = result_people.unique().scalars().all()
        people_dto = [FullPeople.model_validate(row, from_attributes=True) for row in people_models]
        for i in people_dto:
            dict_temp = {'model': 'people', 'fields': {}}
            dict_temp['fields']['id_people'] = i.id_people
            dict_temp['fields']['first_name'] = i.first_name
            dict_temp['fields']['last_name'] = i.last_name
            dict_temp['fields']['patronymic'] = i.patronymic
            dict_temp['fields']['id_point'] = i.id_point
            dict_temp['fields']['id_position'] = i.id_position
            dict_temp['fields']['driving_licence'] = i.driving_licence
            all_data.append(dict_temp)

        query_car = select(Car)
        result_car = await session.execute(query_car)
        car_models = result_car.unique().scalars().all()
        car_dto = [FullCar.model_validate(row, from_attributes=True) for row in car_models]
        for i in car_dto:
            dict_temp = {'model': 'car', 'fields': {}}
            dict_temp['fields']['id_car'] = i.id_car
            dict_temp['fields']['name'] = i.name_car
            dict_temp['fields']['number'] = i.number_of_car
            dict_temp['fields']['average'] = i.average_consumption
            dict_temp['fields']['people'] = i.id_people
            all_data.append(dict_temp)

        query_car_fuel = select(CarFuel)
        result_car_fuel = await session.execute(query_car_fuel)
        car_fuel_models = result_car_fuel.unique().scalars().all()
        car_fuel_dto = [FullCarFuel.model_validate(row, from_attributes=True) for row in car_fuel_models]
        for i in car_fuel_dto:
            dict_temp = {'model': 'car_fuel', 'fields': {}}
            dict_temp['fields']['id_car_fuel'] = i.id_car_fuel
            dict_temp['fields']['car'] = i.id_car
            dict_temp['fields']['fuel'] = i.id_fuel
            all_data.append(dict_temp)

        query_driver = select(Driver)
        result_driver = await session.execute(query_driver)
        driver_models = result_driver.unique().scalars().all()
        driver_dto = [FullDriver.model_validate(row, from_attributes=True) for row in driver_models]
        for i in driver_dto:
            dict_temp = {'model': 'drivers', 'fields': {}}
            dict_temp['fields']['id_driver'] = i.id_driver
            dict_temp['fields']['driver'] = i.id_people
            dict_temp['fields']['date'] = str(i.date_trip)
            all_data.append(dict_temp)

        query_passenger = select(Passenger)
        result_passenger = await session.execute(query_passenger)
        passenger_models = result_passenger.unique().scalars().all()
        passenger_dto = [FullPassenger.model_validate(row, from_attributes=True) for row in passenger_models]
        for i in passenger_dto:
            dict_temp = {'model': 'passengers', 'fields': {}}
            dict_temp['fields']['id_passenger'] = i.id_passenger
            dict_temp['fields']['order'] = i.order
            dict_temp['fields']['passenger'] = i.id_people
            dict_temp['fields']['driver'] = i.id_driver
            dict_temp['fields']['WD'] = i.where_drive
            all_data.append(dict_temp)

        query_refueling = select(Refueling)
        result_refueling = await session.execute(query_refueling)
        refueling_models = result_refueling.unique().scalars().all()
        refueling_dto = [FullRefueling.model_validate(row, from_attributes=True) for row in refueling_models]
        for i in refueling_dto:
            dict_temp = {'model': 'refueling', 'fields': {}}
            dict_temp['fields']['id_refueling'] = i.id_refueling
            dict_temp['fields']['fuel'] = i.id_fuel
            dict_temp['fields']['people'] = i.id_people
            dict_temp['fields']['quantity'] = i.quantity
            dict_temp['fields']['date'] = str(i.date_refueling)
            all_data.append(dict_temp)

        return all_data



if __name__ == '__main__':
    with open(full_path, "w") as write_file:
        json.dump(asyncio.get_event_loop().run_until_complete(download_all()), write_file)

