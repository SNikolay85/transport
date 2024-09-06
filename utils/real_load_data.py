import asyncio
from datetime import datetime

import os
import json

from trips.models import Point, Route, Car, CarFuel, Position, People, Driver, Passenger, Fuel, WhereDrive, Refueling
from trips.models import create_tables, delete_tables, Session_real


current = os.getcwd()
file_name_base = '../real_download_data.json'
full_path = os.path.join(current, file_name_base)

with open(full_path, 'r', encoding='utf-8') as file:
    data_base = json.load(file)


session = Session_real()


async def reboot_tables():
    await delete_tables()
    await create_tables()


async def load_db(data_trans):
    for record in data_trans:
        if record['model'] == 'point':
            point = Point(
                id_point=record['fields']['id_point'],
                name_point=record['fields']['name'],
                latitude=record['fields']['latitude'],
                longitude=record['fields']['longitude'],
                cost=record['fields']['cost'])
            session.add(point)
            await session.commit()
        elif record['model'] == 'route':
            route = Route(
                id_route=record['fields']['id_route'],
                id_start_point=record['fields']['start'],
                id_finish_point=record['fields']['finish'],
                distance=record['fields']['distance'])
            session.add(route)
            await session.commit()
        elif record['model'] == 'car':
            car = Car(
                id_car=record['fields']['id_car'],
                name_car=record['fields']['name'],
                number_of_car=record['fields']['number'],
                average_consumption=record['fields']['average'],
                id_people=record['fields']['people'])
            session.add(car)
            await session.commit()
        elif record['model'] == 'fuel':
            fuel = Fuel(
                id_fuel=record['fields']['id_fuel'],
                name_fuel=record['fields']['name'])
            session.add(fuel)
            await session.commit()
        elif record['model'] == 'where_drive':
            where_drive = WhereDrive(
                id_wd=record['fields']['id_wd'],
                name_wd=record['fields']['name'])
            session.add(where_drive)
            await session.commit()
        elif record['model'] == 'car_fuel':
            car_fuel = CarFuel(
                id_car_fuel=record['fields']['id_car_fuel'],
                id_car=record['fields']['car'],
                id_fuel=record['fields']['fuel'])
            session.add(car_fuel)
            await session.commit()
        elif record['model'] == 'position':
            position = Position(
                id_position=record['fields']['id_position'],
                name_position=record['fields']['name'])
            session.add(position)
            await session.commit()
        elif record['model'] == 'people':
            people = People(
                id_people=record['fields']['id_people'],
                first_name=record['fields']['first_name'],
                last_name=record['fields']['last_name'],
                patronymic=record['fields']['patronymic'],
                id_point=record['fields']['id_point'],
                id_position=record['fields']['id_position'],
                driving_licence=record['fields'].setdefault('driving_licence', None))
            session.add(people)
            await session.commit()
        elif record['model'] == 'drivers':
            date_format = datetime.strptime(record['fields']['date'], '%Y-%m-%d').date()
            drivers = Driver(
                id_driver=record['fields']['id_driver'],
                id_people=record['fields']['driver'],
                date_trip=date_format)
            session.add(drivers)
            await session.commit()
        elif record['model'] == 'passengers':
            passenger = Passenger(
                id_passenger=record['fields']['id_passenger'],
                order=record['fields']['order'],
                id_people=record['fields']['passenger'],
                id_driver=record['fields']['driver'],
                where_drive=record['fields']['WD'])
            session.add(passenger)
            await session.commit()
        elif record['model'] == 'refueling':
            date_format = datetime.strptime(record['fields']['date'], '%Y-%m-%d').date()
            refueling = Refueling(
                id_refueling=record['fields']['id_refueling'],
                id_fuel=record['fields']['fuel'],
                id_people=record['fields']['people'],
                quantity=record['fields']['quantity'],
                date_refueling=date_format)
            session.add(refueling)
            await session.commit()

    await asyncio.shield(session.close())
    return print('Данные считаны и загружены в БД')

if __name__ == '__main__':
    # asyncio.get_event_loop().run_until_complete(reboot_tables())
    # #asyncio.run(reboot_tables())
    # print('Таблицы пересозданы')
    asyncio.get_event_loop().run_until_complete(load_db(data_base))
    # asyncio.run(load_db(data_base))