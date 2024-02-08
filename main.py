import sqlalchemy
from sqlalchemy.orm import sessionmaker

from models import create_tables, People, Point, Position, Transport, Car_Fuel, Fuel, Route, Car

DSN = 'postgresql://postgres:postgres@localhost:5432/trans_db'
engine = sqlalchemy.create_engine(DSN)

Session = sessionmaker(bind=engine)
session = Session()

create_tables(engine)

session.close()