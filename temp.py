import asyncio
import re
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


fg = asyncio.run(UtilityFunction.id_people('пешилов Николай Юрьевич'))
if fg == 0:
    print(f'вас нет в базе')
elif fg == -1:
    print(f'неправельно ввели данные')
else:
    print(fg)

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

# print(asyncio.run(Operation.id_factory()))
# print()
# print(asyncio.run(get_id_factory()))
#print(list(Fuel))
#pprint(asyncio.run(DataGet.find_all_point()))
#pprint(asyncio.run(DataGet.find_all_people()))
#pprint(asyncio.run(DataGet.find_all_car()))
#pprint(asyncio.run(DataGet.find_point_with_people()))
#pprint(asyncio.run(get_driver()))
