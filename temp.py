import asyncio
import json
import os
from hashlib import md5
from pprint import pprint
from typing import Optional
import requests
from pydantic import BaseModel

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import String, ForeignKey, MetaData, Date, DateTime, TIMESTAMP, select
from sqlalchemy.orm import DeclarativeBase, relationship, mapped_column, Mapped, selectinload, joinedload
from sqlalchemy.sql import func
from datetime import datetime, date
# joinedload for many-to-one, one-to-one
# selectinload for one-to-many, many-to-many
from typing_extensions import Annotated

from config import PG_DB, PG_USER, PG_PASSWORD, PG_HOST, PG_PORT, PPR
from trips.models import Session, Point, Car, Driver, People, Position, Refueling, Fuel
from trips.reposit import UtilityFunction
from trips.schema import FullPointRe, FullPeopleRe, PointDrivingLicenceRe, FullDriverRe, FullCarRe, FullPeople, \
    FullFuel, FullRefuelingRe, FullRefueling

from fastapi import FastAPI, Body
from fastapi.responses import FileResponse
#
# date_now = datetime.strftime(datetime.now(), '%Y-%m-%d')
# date_start = datetime.strftime(datetime.today().replace(day=1), '%Y-%m-%d')


def ppr(date_from, date_to, data_format='json'):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': PPR
    }
    data = {'dateFrom': date_from, 'dateTo': date_to, 'format': data_format}
    res = requests.get(f'https://online.petrolplus.ru/api/public-api/v2/transactions',
                       data,
                       headers=headers).json()
    return res['transactions']

ss ='2024-09-29 12:08'
pp = '2024-09-29T11:36:47.000'

date_now = datetime.strptime(ss, '%Y-%m-%d %H:%M')
print(date_now, type(date_now))

print(f'{pp[:10]} {pp[11:19]}')
date_now = datetime.strptime(f'{pp[:10]} {pp[11:23]}', '%Y-%m-%d %H:%M:%S.%f')
print(date_now, type(date_now))


#pprint([{'date': i['date'], 'quantity': i['amount']} for i in ppr(date_start, date_now)])
# print(datetime.strptime('2024-09-01', '%Y-%m-%d %H:%M').date())
async def peoples(ppr_card):
    async with Session() as session:
        q = (
            select(People.id_people)
            .filter(People.ppr_card == ppr_card)
        )
        result = await session.execute(q)
        models = result.unique().scalars().first()
        return models

async def fuels(name):
    async with Session() as session:
        q = (
            select(Fuel.id_fuel)
            .filter(Fuel.name_fuel == name)
        )
        result = await session.execute(q)
        models = result.unique().scalars().first()
        return models

#print(asyncio.run(dddd()))

async def add_refueling(ppr, peoples, fuels):
    date_now = datetime.strftime(datetime.now(), '%Y-%m-%d')
    date_start = datetime.strftime(datetime.today().replace(day=1), '%Y-%m-%d')
    hh = []
    async with Session() as session:
        query = (
            select(Refueling)
            # .options(joinedload(Refueling.fuel), joinedload(Refueling.people))
            .filter(Refueling.date_refueling >= datetime.strptime(date_start, '%Y-%m-%d').date())
        )
        result = await session.execute(query)
        models = result.unique().scalars().all()
        sum_quantity = 0
        for i in models:
            sum_quantity += i.quantity
        sum_ppr = 0
        for i in ppr(date_start, date_now):
            sum_ppr += i['amount']
        list_date = [i['date'] for i in ppr(date_start, date_now)]
        #dto = [FullRefuelingRe.model_validate(row, from_attributes=True) for row in models]
        # ccx = [{
        #     'id_fuel': i.fuel.name_fuel,
        #     'id_people': i.people.ppr_card,
        #     'quantity': i.quantity,
        #     'date_refueling': str(i.date_refueling)} for i in dto]
        # ppr = [{
        #         'id_fuel': i['serviceName'],
        #         'id_people': str(i['cardNum']),
        #         'quantity': i['amount'],
        #         'date_refueling': i['date'][:10]} for i in ppr(date_start, date_now)]
        # for i in ppr:
        #     if i not in ccx:
        #         i['id_fuel'] = await fuels(i['id_fuel'])
        #         i['id_people'] = await peoples(i['id_people'])
        #         i['date_refueling'] = datetime.strptime(i['date_refueling'], '%Y-%m-%d').date()
        #         # datetime.strptime(date_start, '%Y-%m-%d').date()
        #         hh.append(i)
        # query = select(Refueling.id_refueling)
        # result = await session.execute(query)
        # models = result.unique().scalars().all()
        # refuelings = []
        # count_id = await UtilityFunction.get_id(models)
        # for i in hh:
        #     refuelings.append(Refueling(**(dict(i)), id_refueling=count_id))
        #     count_id += 1
        # session.add_all(refuelings)
        # await session.commit()
        # data = {'id_fuel': re
    # id_people: int
    # quantity: float
    # date_refueling: date'}
    #
    #     refueling = Refueling(**(data.model_dump()), id_refueling=await UtilityFunction.get_id(models))
    #     session.add(refueling)
    #     await session.flush()
    #     await session.commit()
        return sum_quantity, sum_ppr, list_date[0]



print(asyncio.run(add_refueling(ppr, peoples, fuels)))
#print(type(asyncio.run(add_refueling(ppr))[0]['quantity']))
async def my_round(num):
    return num if num % 5 == 0 else num + (5 - (num % 5))


#print(datetime.strptime('2024-09-02 23:59:59.999999+00:00',
           #       '%Y-%m-%d %H:%M:%S.%f%z'))


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
async def get_driver():
    driver = await DataGet.find_all_driver()
    return driver
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
#pprint(asyncio.run(get_driver()))
