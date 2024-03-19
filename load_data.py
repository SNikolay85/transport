import asyncio
from datetime import datetime
from time import sleep

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import os
import json
from config import PG_DB, PG_USER, PG_PASSWORD, PG_HOST, PG_PORT

from trips.models import Point, Route, Fuel, Car, CarFuel, \
    Position, People, WhereDrive, Drivers, Passengers, create_tables, delete_tables

PG_DSN = f"postgresql+asyncpg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"

engine = create_async_engine(PG_DSN)

Session = async_sessionmaker(engine, expire_on_commit=False)

current = os.getcwd()
file_name_base = 'test_data.json'
full_path = os.path.join(current, file_name_base)

with open(full_path, 'r', encoding='utf-8') as file:
    data_base = json.load(file)


session = Session()


async def reboot_tables():
    await delete_tables()
    await create_tables()


async def load_db(data_trans):
    for record in data_trans:
        if record['model'] == 'point':
            point = Point(name_point=record['fields']['name'],
                          cost=record['fields']['cost'])
            session.add(point)
            await session.commit()
        elif record['model'] == 'route':
            route = Route(id_start_route=record['fields']['start'],
                          id_finish_route=record['fields']['finish'],
                          distance=record['fields']['distance'])
            session.add(route)
            await session.commit()
        elif record['model'] == 'fuel':
            fuel = Fuel(name_fuel=record['fields']['name'])
            session.add(fuel)
            await session.commit()
        elif record['model'] == 'car':
            car = Car(name_car=record['fields']['name'],
                      number_of_car=record['fields']['number'],
                      average_consumption=record['fields']['average'])
            session.add(car)
            await session.commit()
        elif record['model'] == 'car_fuel':
            car_fuel = CarFuel(id_car=record['fields']['car'],
                               id_fuel=record['fields']['fuel'])
            session.add(car_fuel)
            await session.commit()
        elif record['model'] == 'position':
            position = Position(name_position=record['fields']['name'])
            session.add(position)
            await session.commit()
        elif record['model'] == 'people':
            people = People(first_name=record['fields']['first_name'],
                            last_name=record['fields']['last_name'],
                            patronymic=record['fields']['patronymic'],
                            id_point=record['fields']['id_point'],
                            id_position=record['fields']['id_position'],
                            driving_licence=record['fields'].setdefault('driving_licence', None),
                            id_car=record['fields'].setdefault('id_car', None))
            session.add(people)
            await session.commit()
        elif record['model'] == 'where_drive':
            where_drive = WhereDrive(name_wd=record['fields']['name'])
            session.add(where_drive)
            await session.commit()
        elif record['model'] == 'drivers':
            date_format = datetime.strptime(record['fields']['date'], '%Y-%m-%d').date()
            drivers = Drivers(driver=record['fields']['driver'],
                              date_trip=date_format)
            session.add(drivers)
            await session.commit()
        elif record['model'] == 'passengers':
            passenger = Passengers(order=record['fields']['order'],
                                   passenger=record['fields']['passenger'],
                                   driver=record['fields']['driver'],
                                   id_where_drive=record['fields']['WD'])
            session.add(passenger)
            await session.commit()
    await session.close()
    return print('Данные считаны и загружены в БД')


if __name__ == '__main__':
    # asyncio.get_event_loop().run_until_complete(reboot_tables())
    asyncio.run(reboot_tables())
    print('Таблицы пересозданы')
    # # asyncio.get_event_loop().run_until_complete(load_db(data_base))
    asyncio.run(load_db(data_base))
    # print('первый транш')
    #asyncio.run(load_db(data_next))

    #asyncio.run(session.close())

