import sqlalchemy
from sqlalchemy.orm import sessionmaker
import os
import json
from config import PG_DB, PG_USER, PG_PASSWORD, PG_HOST, PG_PORT

from trips.models import Point, Route, Fuel, Car, CarFuel, \
    Position, People, WhereDrive, Drivers, Passengers

DSN = f'postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}'

def load_db(data_trans):
    for record in data_trans:
        if record['model'] == 'point':
            point = Point(name_point=record['fields']['name'],
                          cost=record['fields']['cost'])
            session.add(point)
            session.commit()
        elif record['model'] == 'route':
            route = Route(id_start_route=record['fields']['start'],
                          id_finish_route=record['fields']['finish'],
                          distance=record['fields']['distance'])
            session.add(route)
            session.commit()
        elif record['model'] == 'fuel':
            fuel = Fuel(name_fuel=record['fields']['name'])
            session.add(fuel)
            session.commit()
        elif record['model'] == 'car':
            car = Car(name_car=record['fields']['name'],
                      number_of_car=record['fields']['number'],
                      average_consumption=record['fields']['average'])
            session.add(car)
            session.commit()
        elif record['model'] == 'car_fuel':
            car_fuel = CarFuel(id_car=record['fields']['car'],
                               id_fuel=record['fields']['fuel'])
            session.add(car_fuel)
            session.commit()
        elif record['model'] == 'position':
            position = Position(name_position=record['fields']['name'])
            session.add(position)
            session.commit()
        elif record['model'] == 'people':
            people = People(first_name=record['fields']['first_name'],
                            last_name=record['fields']['last_name'],
                            patronymic=record['fields']['patronymic'],
                            id_point=record['fields']['id_point'],
                            id_position=record['fields']['id_position'],
                            driving_licence=record['fields'].setdefault('driving_licence', None),
                            id_car=record['fields'].setdefault('id_car', None))
            session.add(people)
            session.commit()
        elif record['model'] == 'where_drive':
            where_drive = WhereDrive(name_wd=record['fields']['name'])
            session.add(where_drive)
            session.commit()
        elif record['model'] == 'drivers':
            drivers = Drivers(driver=record['fields']['driver'],
                              date=record['fields']['date'])
            session.add(drivers)
            session.commit()
        elif record['model'] == 'passengers':
            passenger = Passengers(order=record['fields']['order'],
                                   passenger=record['fields']['passenger'],
                                   driver=record['fields']['driver'],
                                   id_where_drive=record['fields']['WD'])
            session.add(passenger)
            session.commit()
    return print('Данные считаны и загружены в БД')


if __name__ == '__main__':
    engine = sqlalchemy.create_engine(DSN)

    Session = sessionmaker(bind=engine)

    current = os.getcwd()
    file_name = 'test_data.json'
    full_path = os.path.join(current, file_name)

    with open(full_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    session = Session()

    load_db(data)

    session.close()

