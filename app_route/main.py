import sqlalchemy

from sqlalchemy.orm import sessionmaker

from app_route.models.models import People, Point, Route, Drivers, Passengers

from load_data import DSN

engine = sqlalchemy.create_engine(DSN)

Session = sessionmaker(bind=engine)

session = Session()

def list_id_routes(trip):
    id_trip = []
    for i in range(len(trip)-1):
        a, b = trip[i], trip[i+1]
        one_way = session.query(Route).filter(Route.id_start_route == int(a), Route.id_finish_route == int(b)).first()
        other_way = session.query(Route).filter(Route.id_start_route == int(b), Route.id_finish_route == int(a)).first()
        if one_way is None:
            id_trip.append(other_way.id_route)
        else:
            id_trip.append(one_way.id_route)
    return id_trip


def distance_route(list_route):
    route_all = 0
    for i in list_route:
        route_all += session.query(Route).filter(Route.id_route == int(i)).first().distance
    return route_all

def map_route(list_point):
    route = []
    for i in list_point:
        title_point = session.query(Point.name_point).filter(Point.id_point == int(i)).first()
        route.append(title_point.name_point)
    return route


def sum_cost(list_passenger):
    cost = []
    temp = 0
    for i in list_passenger:
        passenger_point = session.query(People.id_point).filter(People.id_people == int(i)).first()
        if passenger_point.id_point == (session.query(People).filter(People.id_people == int(person_id.id_people)).first()).id_point:
            temp += 1
        else:
            cost_check_in = session.query(Point.cost).filter(Point.id_point == int(passenger_point.id_point)).first()
            cost.append(cost_check_in.cost)
    if temp >= 1:
        cost.append(50)
    return sum(cost)

def person_worker(last_name):
    return (session.query(People).
            filter(People.last_name == str(last_name)).
            first()).id_people

name_driver = 'Спешилов'
date_trip = '2024-03-01'
factory = (session.query(Point).filter(Point.name_point == 'Завод').first()).id_point

trip_forward = []
trip_away = []

'''id работника'''
person_id = (session.query(People).
      filter(People.last_name == name_driver).
      first())
'''id работника в качестве водителя'''
driver_id = (session.query(Drivers).
      filter(Drivers.date == date_trip, Drivers.driver == int(person_id.id_people)).
      first())

'''поиск пассажиров на работу за определенную дату c указанным водителем'''
passenger_forward = (session.query(Passengers).
              filter(Passengers.driver == int(driver_id.id_driver), Passengers.id_where_drive == 1).
              order_by(Passengers.order).
              all())
list_passenger_forward = [i.passenger for i in passenger_forward]

'''поиск пассажиров с работы за определенную дату c указанным водителем'''
passenger_away = (session.query(Passengers).
           filter(Passengers.driver == int(driver_id.id_driver), Passengers.id_where_drive == 2).
           order_by(Passengers.order).
           all())
list_passenger_away = [i.passenger for i in passenger_away]

'''построение маршрута на работу'''
trip_forward.append(person_id.id_point)
for i in list_passenger_forward:
    trip_forward.append(session.query(People).filter(People.id_people == int(i)).first().id_point)
trip_forward.append(factory)
trip_forward = list(dict.fromkeys(trip_forward)) # удаление дублей

'''построение маршрута с работы'''
for i in list_passenger_away:
    trip_away.append(session.query(People).filter(People.id_people == int(i)).first().id_point)
trip_away.append(person_id.id_point)
trip_away.insert(0, factory)
trip_away = list(dict.fromkeys(trip_away)) # удаление дублей

'''получение списка фамилий работников из БД'''
person = session.query(People.last_name).all()

'''пример получения данных от web-service'''
record = {
    'id_driver': 21, 'date': '2024-03-01', 'driver': 'Спешилов', 'passengers':
    [
        {'id_pas': 30, 'direction': 1, 'order': 1, 'last_name': 'Чечебейкина'},
        {'id_pas': 31, 'direction': 1, 'order': 2, 'last_name': 'Сидоренкин'},
        {'id_pas': 32, 'direction': 2, 'order': 1, 'last_name': 'Чечебейкина'},
        {'id_pas': 33, 'direction': 2, 'order': 2, 'last_name': 'Сидоренкин'}
    ]
}

# def add_person(data):
#     people = People(id_people=record['pk'],
#                     first_name=record['fields']['first_name'],
#                     last_name=record['fields']['last_name'],
#                     patronymic=record['fields']['patronymic'],
#                     id_point=record['fields']['id_point'],
#                     id_position=record['fields']['id_position'],
#                     driving_licence=record['fields'].setdefault('driving_licence', None),
#                     id_car=record['fields'].setdefault('id_car', None))
#     session.add(people)
#     session.commit()
def add_record(record_answer):
    driver = Drivers(id_driver=record_answer['id_driver'],
                     driver=person_worker(record_answer['driver']),
                     date=record_answer['date'])
    session.add(driver)
    session.commit()
    for i in record_answer['passengers']:
        passengers = Passengers(id_passenger=i['id_pas'],
                                order=i['order'],
                                passenger=person_worker(i['last_name']),
                                driver=driver.id_driver,
                                id_where_drive=i['direction'])
        session.add(passengers)
        session.commit()



#add_record(record)

print(sum_cost(list_passenger_forward))
print(sum_cost(list_passenger_away))
print(map_route(trip_forward))
print(distance_route(list_id_routes(trip_forward)))
print(map_route(trip_away))
print(distance_route(list_id_routes(trip_away)))

# subq = session.query(Drivers).filter(Drivers.date == '2024-10-25').subquery()
# subq1 = session.query(People).join(subq, People.id_people == subq.c.driver).subquery()
# res = session.query(Point).join(subq1, Point.id_point == subq1.c.id_point).all()
# subq2 = session.query(Passengers).filter(Passengers.driver == 1, Passengers.id_where_drive == 1).all()
# list1 = []
# list2 = []
#
# for i in subq2:
#     list1.append(i.passenger)
#     print(i)
# print(list1)
#
# t = session.query(People).join(Drivers.people).all()
# q = session.query(People.last_name,
#                   People.first_name,
#                   Point.name_point,
#                   Position.name_position,
#                   People.driving_licence,
#                   Car.name_car).join(Point).join(Position).join(Car).all()#.join(Car.people).all()


session.close()
