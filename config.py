import os
from dotenv import load_dotenv

load_dotenv()

PG_DB = os.getenv('POSTGRES_DB')
REAL_DB = os.getenv('REAL_DB')
PG_USER = os.getenv('POSTGRES_USER')
PG_PASSWORD = os.getenv('POSTGRES_PASSWORD')
PG_HOST = os.getenv('POSTGRES_HOST')
PG_PORT = os.getenv('POSTGRES_PORT')
TOKEN_ORS = os.getenv('TOKEN_ORS')
SALT = os.getenv('SALT')
PPR = os.getenv('PPR')
