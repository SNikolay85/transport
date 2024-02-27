import sqlalchemy
from sqlalchemy.orm import sessionmaker
import os
import json

from models import create_tables, Point, Route, Fuel, Car, Car_Fuel, Position, People, Where_drive, Drivers, Passengers


def load_db(data_trans):
    for record in data_trans:
        if record['model'] == 'point':
            point = Point(id_point=record['pk'],
                          name_point=record['fields']['name'],
                          cost=record['fields']['cost'])
            session.add(point)
            session.commit()
        elif record['model'] == 'route':
            route = Route(id_route=record['pk'],
                          id_start_route=record['fields']['start'],
                          id_finish_route=record['fields']['finish'],
                          distance=record['fields']['distance'])
            session.add(route)
            session.commit()
        elif record['model'] == 'fuel':
            fuel = Fuel(id_fuel=record['pk'],
                        name_fuel=record['fields']['name'])
            session.add(fuel)
            session.commit()
        elif record['model'] == 'car':
            car = Car(id_car=record['pk'],
                      name_car=record['fields']['name'],
                      number_of_car=record['fields']['number'],
                      average_consumption=record['fields']['average'])
            session.add(car)
            session.commit()
        elif record['model'] == 'car_fuel':
            car_fuel = Car_Fuel(id_car_fuel=record['pk'],
                                id_car=record['fields']['car'],
                                id_fuel=record['fields']['fuel'])
            session.add(car_fuel)
            session.commit()
        elif record['model'] == 'position':
            position = Position(id_position=record['pk'],
                                name_position=record['fields']['name'])
            session.add(position)
            session.commit()
        elif record['model'] == 'people':
            people = People(id_people=record['pk'],
                            first_name=record['fields']['first_name'],
                            last_name=record['fields']['last_name'],
                            patronymic=record['fields']['patronymic'],
                            id_point=record['fields']['id_point'],
                            id_position=record['fields']['id_position'],
                            driving_licence=record['fields']['driving_licence'],
                            id_car=record['fields']['id_car'])
            session.add(people)
            session.commit()
        elif record['model'] == 'where_drive':
            where_drive = Where_drive(id_wd=record['pk'],
                                      name_wd=record['fields']['name'])
            session.add(where_drive)
            session.commit()
        elif record['model'] == 'drivers':
            drivers = Drivers(id_driver=record['pk'],
                              driver=record['fields']['driver'],
                              date=record['fields']['date'])
            session.add(drivers)
            session.commit()
        elif record['model'] == 'passengers':
            passenger = Passengers(id_passenger=record['pk'],
                                   passenger=record['fields']['passenger'],
                                   driver=record['fields']['driver'],
                                   id_where_drive=record['fields']['WD'])
            session.add(passenger)
            session.commit()
    return print('Данные считаны и загружены в БД')


if __name__ == '__main__':

    DSN = 'postgresql://nikolay:nikolay@localhost:5432/trans_db'
    engine = sqlalchemy.create_engine(DSN)

    Session = sessionmaker(bind=engine)

    create_tables(engine)

    current = os.getcwd()
    file_name = 'test_data.json'
    full_path = os.path.join(current, file_name)

    with open(full_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    session = Session()

    load_db(data)

    session.close()
