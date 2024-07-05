import asyncio
from pprint import pprint
from typing import Optional

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




a = r"='1'!DB24+'2'!DB24+'3'!DB24+'4'!DB24+'5'!DB24+'6'!DB24+'7'!DB24+'8'!DB24+'9'!DB24+'10'!DB24+'11'!DB24+'12'!DB24+'13'!DB24+'14'!DB24+'15'!DB24+'16'!DB24+'17'!DB24+'18'!DB24+'19'!DB24+'20'!DB24+'21'!DB24+'22'!DB24+'23'!DB24+'24'!DB24+'25'!DB24+'26'!DB24+'27'!DB24+'28'!DB24+'29'!DB24+'30'!DB24+'31'!DB24"
def replace_str(string):
    b = ['L' if i == 'B' else i for i in string]
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

