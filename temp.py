import asyncio
from pprint import pprint
from typing import Optional
from config import TOKEN_ORS

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import String, ForeignKey, MetaData, Date, DateTime, TIMESTAMP, select
from sqlalchemy.orm import DeclarativeBase, relationship, mapped_column, Mapped, selectinload, joinedload
from sqlalchemy.sql import func
from datetime import datetime, date
# joinedload for many-to-one, one-to-one
# selectinload for one-to-many, many-to-many
from typing_extensions import Annotated

from config import PG_DB, PG_USER, PG_PASSWORD, PG_HOST, PG_PORT
from trips.models import Session, Point, Car, Driver, People, Position
from trips.schema import FullPointRe, FullPeopleRe, PointDrivingLicenceRe, FullDriverRe, FullCarRe


from fastapi import FastAPI, Body
from fastapi.responses import FileResponse

import requests


from geopy.geocoders import Nominatim

def get_geo_position(name: str):
    loc = Nominatim(user_agent="GetLoc")
    get_loc = loc.geocode(name)
    print(f' Полный адрес: {get_loc.address}')
    return get_loc.latitude, get_loc.longitude

name_address = 'Новосемейкино'
# result_geo_position = get_geo_position(name_address)
# print(f' Для названия: {name_address} \n "latitude": {result_geo_position[0]}, "longitude": {result_geo_position[1]}')

def get_name_address(geo_position: str):
    loc = Nominatim(user_agent="GetLoc")
    loc_name = loc.reverse(geo_position)
    return loc_name.address

home_geo = '53.373890, 50.354050'
job_geo = '53.389813, 50.431804'

# result = get_name_address(home_geo)
#
# print(f'Для координат {home_geo} \n адрес: {result}')



route = [[53.389813, 50.431804], [53.25028555, 50.48563977922581]]




def geo_pos(name: str):
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        #'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
        'Accept': 'application/json',
        'Authorization': TOKEN_ORS
    }

    data = {"text": name}
    res = requests.get(f'https://api.openrouteservice.org/geocode/search',
                        headers=headers,
                        json=data).json()
    return res

#print(geo_pos(name_address))

def matrix(locations: list):
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'Accept': 'application/json',
        'Authorization': TOKEN_ORS
    }

    data = {"locations":[i[::-1] for i in locations],"metrics":["distance","duration"],"units":"m"}
    res = requests.post(f'https://api.openrouteservice.org/v2/matrix/driving-car',
                        headers=headers,
                        json=data).json()
    return res['distances'][0][1]

#print(matrix(route) / 1000)


app = FastAPI()


@app.get("/")
def root():
    return FileResponse("trips/templates/test_1.html")


@app.post("/hello")
# def hello(name = Body(embed=True)):
def hello(data=Body()):
    name = data["name"]
    age = data["age"]
    return {"message": f"{name}, ваш возраст - {age}"}




a = r"='1'!ET24+'2'!ET24+'3'!ET24+'4'!ET24+'5'!ET24+'6'!ET24+'7'!ET24+'8'!ET24+'9'!ET24+'10'!ET24+'11'!ET24+'12'!ET24+'13'!ET24+'14'!ET24+'15'!ET24+'16'!ET24+'17'!ET24+'18'!ET24+'19'!ET24+'20'!ET24+'21'!ET24+'22'!ET24+'23'!ET24+'24'!ET24+'25'!ET24+'26'!ET24+'27'!ET24+'28'!ET24+'29'!ET24+'30'!ET24+'31'!ET24"
def replace_str(string):
    b = ['D' if i == 'T' else i for i in string]
    return print("".join(b))

#replace_str(a)


class Operation:
    @classmethod
    async def id_factory(cls):
        async with Session() as session:
            query = select(Point).filter(Point.name_point == 'Завод')
            result = await session.execute(query)
            id_factory = result.scalars().first().id_point
            return id_factory


class DataGet:
    @classmethod
    async def find_all_point(cls):
        async with Session() as session:
            query = select(Point).options(selectinload(Point.peoples))
            result = await session.execute(query)
            point_models = result.unique().scalars().all()
            point_dto = [FullPointRe.model_validate(row, from_attributes=True) for row in point_models]
            return point_dto

    @classmethod
    async def find_all_people(cls):
        async with Session() as session:
            query = (
                select(People)
                .options(joinedload(People.point).load_only(Point.name_point), joinedload(People.position), selectinload(People.cars))
                .limit(3)
            )
            result = await session.execute(query)
            people_models = result.unique().scalars().all()
            people_dto = [FullPeopleRe.model_validate(row, from_attributes=True) for row in people_models]
            return people_dto

    @classmethod
    async def find_point_with_people(cls):
        async with Session() as session:
            query = (
                select(Point)
                .options(selectinload(Point.peoples_driving_licence))
            )
            result = await session.execute(query)
            point_models = result.unique().scalars().all()
            point_dto = [PointDrivingLicenceRe.model_validate(row, from_attributes=True) for row in point_models]
            return point_dto

    @classmethod
    async def find_all_driver(cls):
        async with Session() as session:
            query = (
                select(Driver)
                .options(selectinload(Driver.people))
                .limit(2)
            )
            result = await session.execute(query)
            driver_models = result.unique().scalars().all()
            dr_dto = [FullDriverRe.model_validate(row, from_attributes=True) for row in driver_models]
            return dr_dto

    @classmethod
    async def find_all_car(cls):
        async with Session() as session:
            query = select(Car).options(joinedload(Car.people))
            result = await session.execute(query)
            car_models = result.unique().scalars().all()
            car_dto = [FullCarRe.model_validate(row, from_attributes=True) for row in car_models]
            return car_dto


# async def get_point():
#     points = await DataGet.find_all_point()
#     return {'points': points}
#
#
# async def get_people():
#     people = await DataGet.find_all_people()
#     return people
#
#
# async def get_driver():
#     driver = await DataGet.find_all_driver()
#     return driver
#
#
# async def get_car():
#     car = await DataGet.find_all_car()
#     return {'car': car}
#
#
# async def get_id_factory():
#     factory = await Operation.id_factory()
#     return factory

# print(asyncio.run(Operation.id_factory()))
# print()
# print(asyncio.run(get_id_factory()))
#print(list(Fuel))
#pprint(asyncio.run(DataGet.find_all_point()))
#pprint(asyncio.run(DataGet.find_all_people()))
#pprint(asyncio.run(DataGet.find_all_car()))
#pprint(asyncio.run(DataGet.find_point_with_people()))

