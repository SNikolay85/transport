from sqlalchemy import select
import asyncio
import os
import json

from trips.models import Session, Point, Route, Fuel, Car, CarFuel, Position, Organization
from trips.models import WhereDrive, People, Driver, Passenger, Refueling, OtherRoute

current = os.getcwd()
file_name_base = '../real_download_data.json'
full_path = os.path.join(current, file_name_base)


async def query_data(table):
    async with Session() as session:
        query = select(table)
        result = await session.execute(query)
        models = result.unique().scalars().all()
        return models


async def download_all():
    all_data = []
    for i in await query_data(Point):
        dict_temp = {'model': 'point', 'fields': {}}
        dict_temp['fields']['id_point'] = i.id_point
        dict_temp['fields']['name'] = i.name_point
        dict_temp['fields']['latitude'] = i.latitude
        dict_temp['fields']['longitude'] = i.longitude
        dict_temp['fields']['cost'] = i.cost
        dict_temp['fields']['created_on'] = str(i.created_on)
        dict_temp['fields']['updated_on'] = str(i.updated_on)
        all_data.append(dict_temp)

    for i in await query_data(Route):
        dict_temp = {'model': 'route', 'fields': {}}
        dict_temp['fields']['id_route'] = i.id_route
        dict_temp['fields']['start'] = i.id_start_point
        dict_temp['fields']['finish'] = i.id_finish_point
        dict_temp['fields']['distance'] = i.distance
        dict_temp['fields']['created_on'] = str(i.created_on)
        dict_temp['fields']['updated_on'] = str(i.updated_on)
        all_data.append(dict_temp)

    for i in await query_data(Fuel):
        dict_temp = {'model': 'fuel', 'fields': {}}
        dict_temp['fields']['id_fuel'] = i.id_fuel
        dict_temp['fields']['name'] = i.name_fuel
        dict_temp['fields']['created_on'] = str(i.created_on)
        dict_temp['fields']['updated_on'] = str(i.updated_on)
        all_data.append(dict_temp)

    for i in await query_data(WhereDrive):
        dict_temp = {'model': 'where_drive', 'fields': {}}
        dict_temp['fields']['id_wd'] = i.id_wd
        dict_temp['fields']['name'] = i.name_wd
        dict_temp['fields']['created_on'] = str(i.created_on)
        dict_temp['fields']['updated_on'] = str(i.updated_on)
        all_data.append(dict_temp)

    for i in await query_data(Position):
        dict_temp = {'model': 'position', 'fields': {}}
        dict_temp['fields']['id_position'] = i.id_position
        dict_temp['fields']['name'] = i.name_position
        dict_temp['fields']['created_on'] = str(i.created_on)
        dict_temp['fields']['updated_on'] = str(i.updated_on)
        all_data.append(dict_temp)

    for i in await query_data(People):
        dict_temp = {'model': 'people', 'fields': {}}
        dict_temp['fields']['id_people'] = i.id_people
        dict_temp['fields']['first_name'] = i.first_name
        dict_temp['fields']['last_name'] = i.last_name
        dict_temp['fields']['patronymic'] = i.patronymic
        dict_temp['fields']['id_point'] = i.id_point
        dict_temp['fields']['id_position'] = i.id_position
        dict_temp['fields']['driving_licence'] = i.driving_licence
        dict_temp['fields']['created_on'] = str(i.created_on)
        dict_temp['fields']['updated_on'] = str(i.updated_on)
        all_data.append(dict_temp)

    for i in await query_data(Organization):
        dict_temp = {'model': 'organization', 'fields': {}}
        dict_temp['fields']['id_organization'] = i.id_organization
        dict_temp['fields']['name_organization'] = i.name_organization
        dict_temp['fields']['id_point'] = i.id_point
        dict_temp['fields']['created_on'] = str(i.created_on)
        dict_temp['fields']['updated_on'] = str(i.updated_on)
        all_data.append(dict_temp)

    for i in await query_data(Car):
        dict_temp = {'model': 'car', 'fields': {}}
        dict_temp['fields']['id_car'] = i.id_car
        dict_temp['fields']['name'] = i.name_car
        dict_temp['fields']['number'] = i.number_of_car
        dict_temp['fields']['average'] = i.average_consumption
        dict_temp['fields']['people'] = i.id_people
        dict_temp['fields']['created_on'] = str(i.created_on)
        dict_temp['fields']['updated_on'] = str(i.updated_on)
        all_data.append(dict_temp)

    for i in await query_data(CarFuel):
        dict_temp = {'model': 'car_fuel', 'fields': {}}
        dict_temp['fields']['id_car_fuel'] = i.id_car_fuel
        dict_temp['fields']['car'] = i.id_car
        dict_temp['fields']['fuel'] = i.id_fuel
        dict_temp['fields']['created_on'] = str(i.created_on)
        dict_temp['fields']['updated_on'] = str(i.updated_on)
        all_data.append(dict_temp)

    for i in await query_data(Driver):
        dict_temp = {'model': 'drivers', 'fields': {}}
        dict_temp['fields']['id_driver'] = i.id_driver
        dict_temp['fields']['driver'] = i.id_people
        dict_temp['fields']['date'] = str(i.date_trip)
        dict_temp['fields']['created_on'] = str(i.created_on)
        dict_temp['fields']['updated_on'] = str(i.updated_on)
        all_data.append(dict_temp)

    for i in await query_data(Passenger):
        dict_temp = {'model': 'passengers', 'fields': {}}
        dict_temp['fields']['id_passenger'] = i.id_passenger
        dict_temp['fields']['order'] = i.order
        dict_temp['fields']['passenger'] = i.id_people
        dict_temp['fields']['driver'] = i.id_driver
        dict_temp['fields']['WD'] = i.where_drive
        dict_temp['fields']['created_on'] = str(i.created_on)
        dict_temp['fields']['updated_on'] = str(i.updated_on)
        all_data.append(dict_temp)

    for i in await query_data(OtherRoute):
        dict_temp = {'model': 'other_route', 'fields': {}}
        dict_temp['fields']['id_other_route'] = i.id_other_route
        dict_temp['fields']['order'] = i.order
        dict_temp['fields']['organization'] = i.id_organization
        dict_temp['fields']['driver'] = i.id_driver
        dict_temp['fields']['WD'] = i.where_drive
        dict_temp['fields']['created_on'] = str(i.created_on)
        dict_temp['fields']['updated_on'] = str(i.updated_on)
        all_data.append(dict_temp)

    for i in await query_data(Refueling):
        dict_temp = {'model': 'refueling', 'fields': {}}
        dict_temp['fields']['id_refueling'] = i.id_refueling
        dict_temp['fields']['fuel'] = i.id_fuel
        dict_temp['fields']['people'] = i.id_people
        dict_temp['fields']['quantity'] = float(i.quantity)
        dict_temp['fields']['date'] = str(i.date_refueling)
        dict_temp['fields']['created_on'] = str(i.created_on)
        dict_temp['fields']['updated_on'] = str(i.updated_on)
        all_data.append(dict_temp)

    return all_data


if __name__ == '__main__':
    with open(full_path, "w") as write_file:
        json.dump(asyncio.get_event_loop().run_until_complete(download_all()), write_file)

