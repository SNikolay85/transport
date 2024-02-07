import sqlalchemy
from sqlalchemy.orm import sessionmaker

DSN = 'postgresql://postgres:postgres@localhost:5432/trans_db'
engine = sqlalchemy.create_engine(DSN)

Session = sessionmaker(bind=engine)
session = Session()

session.close()