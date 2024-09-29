import asyncio
from datetime import datetime

import os
import json

from trips.models import Point, Route, Car, CarFuel, Position, People, Driver, Passenger, Fuel
from trips.models import WhereDrive, Refueling, Organization, OtherRoute
from trips.models import create_tables, delete_tables, Session


current = os.getcwd()
file_name_base = '../real_download_data.json'
full_path = os.path.join(current, file_name_base)

with open(full_path, 'r', encoding='utf-8') as file:
    data_base = json.load(file)


session = Session()


async def reboot_tables():
    await delete_tables()
    await create_tables()


def format_date(date_cut=None, date_time=None, date=None):
    if date is not None:
        return datetime.strptime(date, '%Y-%m-%d').date()
    elif date_time is not None:
        return datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S.%f%z')
    else:
        return datetime.strptime(date_cut, '%Y-%m-%d %H:%M:%S')


async def load_db(data_trans):
    for record in data_trans:
        if record['model'] == 'point':
            point = Point(
                id_point=record['fields']['id_point'],
                name_point=record['fields']['name'],
                latitude=record['fields']['latitude'],
                longitude=record['fields']['longitude'],
                cost=record['fields']['cost'],
                created_on=format_date(date_time=record['fields']['created_on']),
                updated_on=format_date(date_time=record['fields']['updated_on'])
            )
            session.add(point)
            await session.commit()
        elif record['model'] == 'route':
            route = Route(
                id_route=record['fields']['id_route'],
                id_start_point=record['fields']['start'],
                id_finish_point=record['fields']['finish'],
                distance=record['fields']['distance'],
                created_on=format_date(date_time=record['fields']['created_on']),
                updated_on=format_date(date_time=record['fields']['updated_on'])
            )
            session.add(route)
            await session.commit()
        elif record['model'] == 'car':
            car = Car(
                id_car=record['fields']['id_car'],
                name_car=record['fields']['name'],
                number_of_car=record['fields']['number'],
                average_consumption=record['fields']['average'],
                id_people=record['fields']['people'],
                created_on=format_date(date_time=record['fields']['created_on']),
                updated_on=format_date(date_time=record['fields']['updated_on'])
            )
            session.add(car)
            await session.commit()
        elif record['model'] == 'fuel':
            fuel = Fuel(
                id_fuel=record['fields']['id_fuel'],
                name_fuel=record['fields']['name'],
                created_on=format_date(date_time=record['fields']['created_on']),
                updated_on=format_date(date_time=record['fields']['updated_on'])
            )
            session.add(fuel)
            await session.commit()
        elif record['model'] == 'where_drive':
            where_drive = WhereDrive(
                id_wd=record['fields']['id_wd'],
                name_wd=record['fields']['name'],
                created_on=format_date(date_time=record['fields']['created_on']),
                updated_on=format_date(date_time=record['fields']['updated_on'])
            )
            session.add(where_drive)
            await session.commit()
        elif record['model'] == 'car_fuel':
            car_fuel = CarFuel(
                id_car_fuel=record['fields']['id_car_fuel'],
                id_car=record['fields']['car'],
                id_fuel=record['fields']['fuel'],
                created_on=format_date(date_time=record['fields']['created_on']),
                updated_on=format_date(date_time=record['fields']['updated_on'])
            )
            session.add(car_fuel)
            await session.commit()
        elif record['model'] == 'position':
            position = Position(
                id_position=record['fields']['id_position'],
                name_position=record['fields']['name'],
                created_on=format_date(date_time=record['fields']['created_on']),
                updated_on=format_date(date_time=record['fields']['updated_on'])
            )
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
                driving_licence=record['fields'].setdefault('driving_licence', None),
                ppr_card=record['fields'].setdefault('ppr_card', None),
                created_on=format_date(date_time=record['fields']['created_on']),
                updated_on=format_date(date_time=record['fields']['updated_on'])
            )
            session.add(people)
            await session.commit()
        elif record['model'] == 'organization':
            organization = Organization(
                id_organization=record['fields']['id_organization'],
                name_organization=record['fields']['name_organization'],
                id_point=record['fields']['id_point'],
                created_on=format_date(date_time=record['fields']['created_on']),
                updated_on=format_date(date_time=record['fields']['updated_on'])
            )
            session.add(organization)
            await session.commit()
        elif record['model'] == 'drivers':
            drivers = Driver(
                id_driver=record['fields']['id_driver'],
                id_people=record['fields']['driver'],
                date_trip=format_date(date=record['fields']['date']),
                where_drive=record['fields']['where_drive'],
                created_on=format_date(date_time=record['fields']['created_on']),
                updated_on=format_date(date_time=record['fields']['updated_on'])
            )
            session.add(drivers)
            await session.commit()
        elif record['model'] == 'passengers':
            passenger = Passenger(
                id_passenger=record['fields']['id_passenger'],
                order=record['fields']['order'],
                id_people=record['fields']['passenger'],
                id_driver=record['fields']['driver'],
                where_drive=record['fields']['WD'],
                created_on=format_date(date_time=record['fields']['created_on']),
                updated_on=format_date(date_time=record['fields']['updated_on'])
            )
            session.add(passenger)
            await session.commit()
        elif record['model'] == 'other_route':
            other_route = OtherRoute(
                id_other_route=record['fields']['id_other_route'],
                order=record['fields']['order'],
                id_organization=record['fields']['organization'],
                id_driver=record['fields']['driver'],
                where_drive=record['fields']['WD'],
                created_on=format_date(date_time=record['fields']['created_on']),
                updated_on=format_date(date_time=record['fields']['updated_on'])
            )
            session.add(other_route)
            await session.commit()
        elif record['model'] == 'refueling':
            refueling = Refueling(
                id_refueling=record['fields']['id_refueling'],
                id_fuel=record['fields']['fuel'],
                id_people=record['fields']['people'],
                quantity=record['fields']['quantity'],
                date_refueling=format_date(date_cut=record['fields']['date']),
                created_on=format_date(date_time=record['fields']['created_on']),
                updated_on=format_date(date_time=record['fields']['updated_on'])
            )
            session.add(refueling)
            await session.commit()

    await asyncio.shield(session.close())
    return print('Данные считаны и загружены в БД')

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(reboot_tables())
    print('Таблицы пересозданы')
    asyncio.get_event_loop().run_until_complete(load_db(data_base))
