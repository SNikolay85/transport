from config import TOKEN_ORS
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

from trips.models import Session, Point, Route, Fuel, Car, CarFuel, Position, Organization
from trips.models import WhereDrive, People, Driver, Passenger, Refueling, OtherRoute

from trips.schema import PointAdd, DriverAdd, PassengerAdd, RouteAdd, CarAdd, CarFuelAdd, PositionAdd, PeopleAdd
from trips.schema import FuelAdd, WhereDriveAdd, RefuelingAdd, OrganizationAdd, OtherRouteAdd

from trips.schema import FullPoint, FullRefueling, FullPeople, FullCar, FullFuel, FullCarFuel, FullRoute
from trips.schema import FullWhereDrive, FullDriver, FullPassenger, FullPosition, FullOrganization, FullOtherRoute

from trips.schema import FullRouteRe, FullRefuelingRe, FullFuelRe, FullWhereDriveRe, FullPositionRe, FullOtherRouteRe
from trips.schema import FullCarRe, FullPeopleRe, FullPointRe, FullDriverRe, NamePoint, FullOrganizationRe
from trips.schema import FullPassengerRe, FullPassengerDriverRe

import requests
from geopy.geocoders import Nominatim

def my_round(num):
    return num if num % 5 == 0 else num + (5 - (num % 5))

def matrix(locations: list):
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'Accept': 'application/json',
        'Authorization': TOKEN_ORS
    }

    data = {"locations": locations, "metrics": ["distance"], "units": "m"}
    res = requests.post(f'https://api.openrouteservice.org/v2/matrix/driving-car',
                        headers=headers,
                        json=data).json()
    return res['distances'][0][1]



class DataLoads:
    @classmethod
    async def get_id(cls, list_id: list) -> int:
        return max(list_id) + 1 if len(list_id) != 0 else 1


    @classmethod
    async def get_geo(cls, data: RouteAdd) -> list:
        list_geo = []
        async with Session() as session:
            query_start_point = select(Point).filter(Point.id_point == data.id_start_point)
            result_qsp = await session.execute(query_start_point)
            qsp_models = result_qsp.unique().scalars().all()
            list_geo.append([qsp_models[0].longitude, qsp_models[0].latitude])

            query_finish_point = select(Point).filter(Point.id_point == data.id_finish_point)
            result_qfp = await session.execute(query_finish_point)
            qfp_models = result_qfp.unique().scalars().all()
            list_geo.append([qfp_models[0].longitude, qfp_models[0].latitude])
            return list_geo


    @classmethod
    async def add_point(cls, data: PointAdd) -> dict:
        loc = Nominatim(user_agent="GetLoc")
        get_location = loc.geocode(data.name_point)
        async with Session() as session:
            query_point = select(Point.id_point)
            result_point = await session.execute(query_point)
            point_models = result_point.unique().scalars().all()
            point = Point(**(data.model_dump()), latitude=get_location.latitude, longitude=get_location.longitude,
                          id_point=await DataLoads.get_id(point_models))
            session.add(point)
            await session.flush()
            await session.commit()
            return {
                "id_point": point.id_point,
                "name_point": point.name_point,
                "cost": point.cost,
                "latitude": point.latitude,
                "longitude": point.longitude
            }

    @classmethod
    async def add_route(cls, data: RouteAdd) -> dict:
        geo_route = await DataLoads.get_geo(data)
        dist = my_round(int(matrix(geo_route) / 1000))
        async with Session() as session:
            query_route = select(Route.id_route)
            result_route = await session.execute(query_route)
            route_models = result_route.unique().scalars().all()
            route = Route(**(data.model_dump()), distance=dist, id_route=await DataLoads.get_id(route_models))
            session.add(route)
            await session.flush()
            await session.commit()
            return {
                "id_route": route.id_route,
                "id_start_point": route.id_start_point,
                "id_finish_point": route.id_finish_point,
                "distance": route.distance
            }

    @classmethod
    async def add_fuel(cls, data: FuelAdd) -> dict:
        async with Session() as session:
            query_fuel = select(Fuel.id_fuel)
            result_fuel = await session.execute(query_fuel)
            fuel_models = result_fuel.unique().scalars().all()
            fuel = Fuel(**(data.model_dump()), id_fuel=await DataLoads.get_id(fuel_models))
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
            query_car = select(Car.id_car)
            result_car = await session.execute(query_car)
            car_models = result_car.unique().scalars().all()
            car = Car(**(data.model_dump()), id_car=await DataLoads.get_id(car_models))
            session.add(car)
            await session.flush()
            await session.commit()
            return {
                "id_car": car.id_car,
                "name_car": car.name_car,
                "number_of_car": car.number_of_car,
                "average_consumption": car.average_consumption,
                "id_people": car.id_people
            }

    @classmethod
    async def add_car_fuel(cls, data: CarFuelAdd) -> dict:
        async with Session() as session:
            query_car_fuel = select(CarFuel.id_car_fuel)
            result_car_fuel = await session.execute(query_car_fuel)
            car_fuel_models = result_car_fuel.unique().scalars().all()
            car_fuel = CarFuel(**(data.model_dump()), id_car_fuel=await DataLoads.get_id(car_fuel_models))
            session.add(car_fuel)
            await session.flush()
            await session.commit()
            return {
                "id_car_fuel": car_fuel.id_car_fuel,
                "id_car": car_fuel.id_car,
                "fuel": car_fuel.id_fuel
            }

    @classmethod
    async def add_position(cls, data: PositionAdd) -> dict:
        async with Session() as session:
            query_position = select(Position.id_position)
            result_position = await session.execute(query_position)
            position_models = result_position.unique().scalars().all()
            position = Position(**(data.model_dump()), id_position=await DataLoads.get_id(position_models))
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
            query_wd = select(WhereDrive.id_wd)
            result_wd = await session.execute(query_wd)
            wd_models = result_wd.unique().scalars().all()
            wd = WhereDrive(**(data.model_dump()), id_wd=await DataLoads.get_id(wd_models))
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
            query_people = select(People.id_people)
            result_people = await session.execute(query_people)
            people_models = result_people.unique().scalars().all()
            people = People(**(data.model_dump()), id_people=await DataLoads.get_id(people_models))
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
                "driving_licence": people.driving_licence
            }

    @classmethod
    async def add_organization(cls, data: OrganizationAdd) -> dict:
        async with Session() as session:
            query_organization = select(Organization.id_organization)
            result_organization = await session.execute(query_organization)
            organization_models = result_organization.unique().scalars().all()
            organization = Organization(**(data.model_dump()), id_organization=await DataLoads.get_id(organization_models))
            session.add(organization)
            await session.flush()
            await session.commit()
            return {
                "id_organization": organization.id_organization,
                "name_organization": organization.name_organization,
                "id_point": organization.id_point
            }

    @classmethod
    async def add_driver(cls, data: DriverAdd) -> dict:
        async with Session() as session:
            query_driver = select(Driver.id_driver)
            result_driver = await session.execute(query_driver)
            driver_models = result_driver.unique().scalars().all()
            driver = Driver(**(data.model_dump()), id_driver=await DataLoads.get_id(driver_models))
            session.add(driver)
            await session.flush()
            await session.commit()
            return {
                "id_driver": driver.id_driver,
                "id_people": driver.id_people,
                "date_trip": driver.date_trip
            }

    @classmethod
    async def add_passenger(cls, data: PassengerAdd) -> dict:
        async with Session() as session:
            query_passenger = select(Passenger.id_passenger)
            result_passenger = await session.execute(query_passenger)
            passenger_models = result_passenger.unique().scalars().all()
            passenqer = Passenger(**(data.model_dump()), id_passenger=await DataLoads.get_id(passenger_models))
            session.add(passenqer)
            await session.flush()
            await session.commit()
            return {
                "id_passenger": passenqer.id_passenger,
                "order": passenqer.order,
                "id_people": passenqer.id_people,
                "id_driver": passenqer.id_driver,
                "where_drive": passenqer.where_drive
            }

    @classmethod
    async def add_other_route(cls, data: OtherRouteAdd) -> dict:
        async with Session() as session:
            query_other_route = select(OtherRoute.id_other_route)
            result_other_route = await session.execute(query_other_route)
            other_route_models = result_other_route.unique().scalars().all()
            other_route = OtherRoute(**(data.model_dump()), id_other_route=await DataLoads.get_id(other_route_models))
            session.add(other_route)
            await session.flush()
            await session.commit()
            return {
                "id_other_route": other_route.id_other_route,
                "order": other_route.order,
                "id_organization": other_route.id_organization,
                "id_driver": other_route.id_driver,
                "where_drive": other_route.where_drive
            }

    @classmethod
    async def add_refueling(cls, data: RefuelingAdd) -> dict:
        async with Session() as session:
            query_refueling = select(Refueling.id_refueling)
            result_refueling = await session.execute(query_refueling)
            refueling_models = result_refueling.unique().scalars().all()
            refueling = Refueling(**(data.model_dump()), id_refueling=await DataLoads.get_id(refueling_models))
            session.add(refueling)
            await session.flush()
            await session.commit()
            return {
                "id_refueling": refueling.id_refueling,
                "id_fuel": refueling.id_fuel,
                "id_people": refueling.id_people,
                "quantity": refueling.quantity,
                "date_refueling": refueling.date_refueling
            }



class DataGet:
    @staticmethod
    async def list_id_routes(trip):
        async with Session() as session:
            id_trip = []
            for i in range(len(trip) - 1):
                a, b = trip[i], trip[i + 1]
                rrr = await session.execute(select(Route).filter(Route.id_start_point == int(a),
                                                      Route.id_finish_point == int(b)))
                one_way = rrr.unique().scalars().first()
                eee = await session.execute(select(Route).filter(Route.id_start_point == int(b),
                                                        Route.id_finish_point == int(a)))
                other_way = eee.unique().scalars().first()
                if one_way is None:
                    id_trip.append(other_way.id_route)
                else:
                    id_trip.append(one_way.id_route)
            route_all = 0
            for i in id_trip:
                ggg = await session.execute(select(Route).filter(Route.id_route == int(i)))
                route_all += ggg.unique().scalars().first().distance
            return route_all

    @staticmethod
    async def all_name_point():
        async with Session() as session:
            query = select(Point)
            result = await session.execute(query)
            point_models = result.unique().scalars().all()
            point_dto = [NamePoint.model_validate(row, from_attributes=True) for row in point_models]
            dict_points = {int(i.id_point):i.name_point for i in point_dto}
            return dict_points

    @staticmethod
    async def all_point():
        async with Session() as session:
            query = select(Point)
            result = await session.execute(query)
            point_models = result.unique().scalars().all()
            point_dto = [FullPoint.model_validate(row, from_attributes=True) for row in point_models]
            return point_dto

    @staticmethod
    async def find_all_point():
        async with Session() as session:
            query = select(Point).options(selectinload(Point.peoples))
            result = await session.execute(query)
            point_models = result.unique().scalars().all()
            point_dto = [FullPointRe.model_validate(row, from_attributes=True) for row in point_models]
            return point_dto

    @staticmethod
    async def find_name_point(name_point: str):
        async with Session() as session:
            query = select(Point).options(selectinload(Point.peoples)).filter(Point.name_point == name_point)
            result = await session.execute(query)
            point_models = result.unique().scalars().all()
            point_dto = [FullPointRe.model_validate(row, from_attributes=True) for row in point_models]
            return point_dto

    @classmethod
    async def find_all_route(cls):
        async with (Session() as session):
            query = (
                select(Route)
                .options(joinedload(Route.point_start), joinedload(Route.point_finish))
                .limit(10)
            )
            result = await session.execute(query)
            route_models = result.scalars().all()
            route_dto = [FullRouteRe.model_validate(row, from_attributes=True) for row in route_models]
            return route_dto

    @classmethod
    async def find_all_fuel(cls):
        async with Session() as session:
            query = (
                select(Fuel)
                .options(selectinload(Fuel.refuelings))
            )
            result = await session.execute(query)
            fuel_models = result.scalars().all()
            fuel_dto = [FullFuelRe.model_validate(row, from_attributes=True) for row in fuel_models]
            return fuel_dto

    @classmethod
    async def find_all_car(cls):
        async with Session() as session:
            query = select(Car).options(joinedload(Car.people))
            result = await session.execute(query)
            car_models = result.unique().scalars().all()
            car_dto = [FullCarRe.model_validate(row, from_attributes=True) for row in car_models]
            return car_dto


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
            query = (
                select(Position)
                .options(selectinload(Position.peoples))
            )
            result = await session.execute(query)
            position_models = result.scalars().all()
            position_dto = [FullPositionRe.model_validate(row, from_attributes=True) for row in position_models]
            return position_dto

    @classmethod
    async def find_all_wd(cls):
        async with Session() as session:
            query = (
                select(WhereDrive)
                .options(selectinload(WhereDrive.passengers))
            )
            result = await session.execute(query)
            wd_models = result.scalars().all()
            wd_dto = [FullWhereDriveRe.model_validate(row, from_attributes=True) for row in wd_models]
            return wd_dto

    @classmethod
    async def find_all_people(cls):
        async with Session() as session:
            query = (
                select(People)
                .options(joinedload(People.point))
                .options(joinedload(People.position))
                .options(selectinload(People.cars))
                .limit(20)
            )
            result = await session.execute(query)
            people_models = result.unique().scalars().all()
            people_dto = [FullPeopleRe.model_validate(row, from_attributes=True) for row in people_models]
            return people_dto

    @classmethod
    async def find_all_organization(cls):
        async with Session() as session:
            query = (
                select(Organization)
                .options(joinedload(Organization.point))
            )
            result = await session.execute(query)
            organization_models = result.unique().scalars().all()
            organization_dto = [FullOrganizationRe.model_validate(row, from_attributes=True) for row in organization_models]
            return organization_dto

    @classmethod
    async def find_user(cls, user_id: int):
        async with Session() as session:
            query = (
                select(People)
                    .options(joinedload(People.point))
                    .options(joinedload(People.position))
                    .options(selectinload(People.cars))
                    .filter(People.id_people == user_id)
            )
            result = await session.execute(query)
            people_models = result.unique().scalars().all()
            people_dto = [FullPeopleRe.model_validate(row, from_attributes=True) for row in people_models]
            return people_dto

    @classmethod
    async def find_all_driver(cls):
        async with Session() as session:
            query = (
                select(People)
                .options(joinedload(People.point))
                .options(joinedload(People.position))
                .options(selectinload(People.cars))
                .filter(People.driving_licence != '')
                .limit(50)
            )
            result = await session.execute(query)
            people_models = result.unique().scalars().all()
            people_dto = [FullPeopleRe.model_validate(row, from_attributes=True) for row in people_models]
            return people_dto


    @classmethod
    async def find_driver_of_date(cls, now_date_trip):
        async with Session() as session:
            query = (
                select(Driver)
                .options(joinedload(Driver.people))
                .filter(Driver.date_trip == now_date_trip)
                .limit(10)
            )
            result = await session.execute(query)
            drivers_models = result.unique().scalars().all()
            driver_dto = [FullDriverRe.model_validate(row, from_attributes=True) for row in drivers_models]
            return driver_dto

    @classmethod
    async def find_passenger_of_driver(cls, id_driver, wd):
        async with Session() as session:
            query = (
                select(Passenger)
                .options(joinedload(Passenger.people))
                .options(joinedload(Passenger.wd))
                .filter(Passenger.id_driver == id_driver, Passenger.where_drive == wd)
                .limit(10)
            )
            result = await session.execute(query)
            models = result.unique().scalars().all()
            dto = [FullPassengerDriverRe.model_validate(row, from_attributes=True) for row in models]
            if wd == 1:
                list_id_point_forward = []
                query = select(Driver.id_people).filter(Driver.id_driver == id_driver)
                result = await session.execute(query)
                md = result.unique().scalars().first()
                query = select(People.id_point).filter(People.id_people == md)
                result = await session.execute(query)
                list_id_point_forward.append(result.unique().scalars().first())
                list_id_point_forward.extend([i.people.id_point for i in dto])
                query = select(Point.id_point).filter(Point.name_point == 'Завод')
                result = await session.execute(query)
                list_id_point_forward.append(result.unique().scalars().first())
                ss = await DataGet.list_id_routes(list_id_point_forward)
            else:
                ...
            return dto, list_id_point_forward, ss


    @classmethod
    async def find_all_car_carrier(cls):
        async with Session() as session:
            query = (
                select(Driver)
                .options(joinedload(Driver.people))
                .limit(10)
            )
            result = await session.execute(query)
            drivers_models = result.unique().scalars().all()
            driver_dto = [FullDriverRe.model_validate(row, from_attributes=True) for row in drivers_models]
            return driver_dto

    @classmethod
    async def find_all_passengers(cls):
        async with Session() as session:
            query = (
                select(Passenger)
                .options(joinedload(Passenger.people))
                .options(joinedload(Passenger.driver))
                .options(joinedload(Passenger.wd))
            )
            result = await session.execute(query)
            passenger_models = result.scalars().all()
            passenger_dto = [FullPassengerRe.model_validate(row, from_attributes=True) for row in passenger_models]
            return passenger_dto

    @classmethod
    async def find_all_other_route(cls):
        async with Session() as session:
            query = (
                select(OtherRoute)
                .options(joinedload(OtherRoute.organization), joinedload(OtherRoute.driver), joinedload(OtherRoute.wd))
            )
            result = await session.execute(query)
            other_route_models = result.scalars().all()
            other_route_dto = [FullOtherRouteRe.model_validate(row, from_attributes=True) for row in other_route_models]
            return other_route_dto

    @classmethod
    async def find_all_refuelings(cls):
        async with Session() as session:
            query = (
                select(Refueling)
                .options(joinedload(Refueling.fuel), joinedload(Refueling.people))
            )
            result = await session.execute(query)
            refueling_models = result.scalars().all()
            refueling_dto = [FullRefuelingRe.model_validate(row, from_attributes=True) for row in refueling_models]
            return refueling_dto


