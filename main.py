import sqlalchemy

from sqlalchemy.orm import sessionmaker

from models import People, Point, Position, Car_Fuel, Fuel, Route, Car, Where_drive, Drivers, Passengers

from load_data import DSN

engine = sqlalchemy.create_engine(DSN)

Session = sessionmaker(bind=engine)

session = Session()

'''
показать расстояние, которое проехал определенный водитель за определенное число
25.10.2024
'''
subq = session.query(Drivers).filter(Drivers.date == '2024-10-25').subquery()
subq1 = session.query(People).join(subq, People.id_people == subq.c.driver).subquery()
res = session.query(Point).join(subq1, Point.id_point == subq1.c.id_point).all()
list1 = []
list2 = []
print('hello world')
#git remote set-url origin https://github.com/SNikolay85/transport.git

for i in res:
    list1.append(i.id_point)
    print(i)
print(list1)

t = session.query(People).join(Drivers.people).all()
q = session.query(People.last_name,
                  People.first_name,
                  Point.name_point,
                  Position.name_position,
                  People.driving_licence,
                  Car.name_car).join(Point).join(Position).join(Car).all()#.join(Car.people).all()


session.close()
