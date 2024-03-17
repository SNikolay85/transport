from sqlalchemy import select

from trips.models import Session, Point, Route, Fuel, Car, CarFuel, Position
from trips.models import WhereDrive, People, Drivers, Passengers
from trips.schema import PointAdd, RouteAdd, FuelAdd, CarAdd, CarFuelAdd
from trips.schema import PositionAdd, WhereDriveAdd, PeopleAdd, DriverAdd, PassengerAdd
import asyncio


class DataLoads:
    @classmethod
    async def add_point(cls, data: PointAdd) -> dict:
        async with Session() as session:
            point = Point(**(data.model_dump()))
            session.add(point)
            await session.flush()
            await session.commit()
            return {
                "id_point": point.id_point,
                "name": point.name_point,
                "cost": point.cost
            }

    @classmethod
    async def add_route(cls, data: RouteAdd) -> dict:
        async with Session() as session:
            route = Route(**(data.model_dump()))
            session.add(route)
            await session.flush()
            await session.commit()
            return {
                "id_route": route.id_route,
                "id_start_route": route.id_start_route,
                "id_finish_route": route.id_finish_route,
                "distance": route.distance
            }

    @classmethod
    async def add_fuel(cls, data: FuelAdd) -> dict:
        async with Session() as session:
            fuel = Fuel(**(data.model_dump()))
            session.add(fuel)
            await session.flush()
            await session.commit()
            return {
                "id_fuel": fuel.id_fuel,
                "name_fuel": fuel.name_fuel
            }

    @classmethod
    async def add_car(cls, data: CarAdd) -> dict:
        async with Session() as session:
            car = Car(**(data.model_dump()))
            session.add(car)
            await session.flush()
            await session.commit()
            return {
                "id_car": car.id_car,
                "name_car": car.name_car,
                "number_of_car": car.number_of_car,
                "average_consumption": car.average_consumption
            }

    @classmethod
    async def add_car_fuel(cls, data: CarFuelAdd) -> dict:
        async with Session() as session:
            car_fuel = CarFuel(**(data.model_dump()))
            session.add(car_fuel)
            await session.flush()
            await session.commit()
            return {
                "id_car_fuel": car_fuel.id_car_fuel,
                "id_car": car_fuel.id_car,
                "id_fuel": car_fuel.id_fuel
            }

    @classmethod
    async def add_position(cls, data: PositionAdd) -> dict:
        async with Session() as session:
            position = Position(**(data.model_dump()))
            session.add(position)
            await session.flush()
            await session.commit()
            return {
                "id_position": position.id_position,
                "name_position": position.name_position
            }

    @classmethod
    async def add_wd(cls, data: WhereDriveAdd) -> dict:
        async with Session() as session:
            wd = WhereDrive(**(data.model_dump()))
            session.add(wd)
            await session.flush()
            await session.commit()
            return {
                "id_wd": wd.id_wd,
                "name_wd": wd.name_wd
            }

    @classmethod
    async def add_people(cls, data: PeopleAdd) -> dict:
        async with Session() as session:
            people = People(**(data.model_dump()))
            session.add(people)
            await session.flush()
            await session.commit()
            return {
                "id_people": people.id_people,
                "first_name": people.first_name,
                "last_name": people.last_name,
                "patronymic": people.patronymic,
                "id_point": people.id_point,
                "id_position": people.id_position,
                "driving_licence": people.driving_licence,
                "id_car": people.id_car
            }

    @classmethod
    async def add_driver(cls, data: DriverAdd) -> dict:
        async with Session() as session:
            driver = Drivers(**(data.model_dump()))
            session.add(driver)
            await session.flush()
            await session.commit()
            return {
                "id_driver": driver.id_driver,
                "driver": driver.driver,
                "date": driver.date
            }

    @classmethod
    async def add_passenger(cls, data: PassengerAdd) -> dict:
        async with Session() as session:
            passenqer = Passengers(**(data.model_dump()))
            session.add(passenqer)
            await session.flush()
            await session.commit()
            return {
                "id_passenger": passenqer.id_passenger,
                "order": passenqer.order,
                "passenger": passenqer.passenger,
                "driver": passenqer.driver,
                "id_where_drive": passenqer.id_where_drive
            }


class DataGet:
    @classmethod
    async def find_all_point(cls):
        async with Session() as session:
            query = select(Point)
            result = await session.execute(query)
            point_models = result.scalars().all()
            return point_models

    @classmethod
    async def find_all_route(cls):
        async with Session() as session:
            query = select(Route)
            result = await session.execute(query)
            route_models = result.scalars().all()
            return route_models

    @classmethod
    async def find_all_fuel(cls):
        async with Session() as session:
            query = select(Fuel)
            result = await session.execute(query)
            fuel_models = result.scalars().all()
            return fuel_models

    @classmethod
    async def find_all_car(cls):
        async with Session() as session:
            query = select(Car)
            result = await session.execute(query)
            car_models = result.scalars().all()
            return car_models

    @classmethod
    async def find_all_car_fuel(cls):
        async with Session() as session:
            query = select(CarFuel)
            result = await session.execute(query)
            car_fuel_models = result.scalars().all()
            return car_fuel_models

    @classmethod
    async def find_all_position(cls):
        async with Session() as session:
            query = select(Position)
            result = await session.execute(query)
            position_models = result.scalars().all()
            return position_models

    @classmethod
    async def find_all_wd(cls):
        async with Session() as session:
            query = select(WhereDrive)
            result = await session.execute(query)
            wd_models = result.scalars().all()
            return wd_models

    @classmethod
    async def find_all_people(cls):
        async with Session() as session:
            query = select(People)
            result = await session.execute(query)
            people_models = result.scalars().all()
            return people_models

    @classmethod
    async def find_all_driver(cls):
        async with Session() as session:
            query = select(Drivers)
            result = await session.execute(query)
            drivers_models = result.scalars().all()
            return drivers_models

    @classmethod
    async def find_all_passengers(cls):
        async with Session() as session:
            query = select(Passengers)
            result = await session.execute(query)
            passenger_models = result.scalars().all()
            return passenger_models
