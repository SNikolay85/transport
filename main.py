import sqlalchemy

from sqlalchemy.orm import sessionmaker

from models import People, Point, Position, Car_Fuel, Fuel, Route, Car, Where_drive, Drivers, Passengers

from load_data import DSN

engine = sqlalchemy.create_engine(DSN)

Session = sessionmaker(bind=engine)

session = Session()

def distance(trip):
    id_trip = []
    for i in range(len(trip)-1):
        a, b = trip[i], trip[i+1]
        q4_1 = session.query(Route).filter(Route.id_start_route == a, Route.id_finish_route == b).first()
        q4_2 = session.query(Route).filter(Route.id_start_route == b, Route.id_finish_route == a).first()
        if q4_1 is None:
            id_trip.append(q4_2.id_route)
        else:
            id_trip.append(q4_1.id_route)
    return id_trip


def sum_route(distance):
    route_all = 0
    for i in distance:
        q5 = session.query(Route).filter(Route.id_route == i).first()
        route_all += q5.distance
    return route_all

'''
показать расстояние, которое проехал определенный водитель за определенное число
25.10.2024
'''
name_driver = 'Урдин'
date_trip = '2024-10-25'
factory = (session.query(Point).filter(Point.name_point == 'Завод').first()).id_point
print(f'{factory} - id завода')
trip_forward = []
trip_away = []

q1 = (session.query(People).
      filter(People.last_name == name_driver).
      first())
print(f'{q1.id_people} - id человека по фамилии Урдин')
trip_forward.append(q1.id_point)
q2 = (session.query(Drivers).
      filter(Drivers.date == date_trip, Drivers.driver == q1.id_people).
      first())
print(f'{q2.id_driver} - id человека в качестве водителя')
q3_forward = (session.query(Passengers).
              filter(Passengers.driver == q2.id_driver, Passengers.id_where_drive == 1).
              order_by(Passengers.order).
              all())
pas_forward = [i.passenger for i in q3_forward]
print(f'{pas_forward} - список id людей на работу')
q3_away = (session.query(Passengers).
           filter(Passengers.driver == q2.id_driver, Passengers.id_where_drive == 2).
           order_by(Passengers.order).
           all())
pas_away = [i.passenger for i in q3_away]
print(f'{pas_away} - список id людей с работы')
for i in pas_forward:
    trip_forward.append(session.query(People).filter(People.id_people == i).first().id_point)
trip_forward.append(factory)
print(f'{trip_forward} - список id точек на маршруте на работу')
for i in pas_away:
    trip_away.append(session.query(People).filter(People.id_people == i).first().id_point)
trip_away.append(q1.id_point)
trip_away.insert(0, factory)
print(f'{trip_away} - список id точек на маршруте с работы')

print(sum_route(distance(trip_forward)))
print(sum_route(distance(trip_away)))

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


#session.close()
