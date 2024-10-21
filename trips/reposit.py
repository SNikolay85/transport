from datetime import datetime
from hashlib import md5

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from config import TOKEN_ORS, SALT, PPR
from sqlalchemy import select, or_, and_, update, delete
from sqlalchemy.orm import selectinload, joinedload

from trips.models import Session, Point, Route, Fuel, Car, CarFuel, Position, Organization
from trips.models import WhereDrive, People, Driver, Passenger, Refueling, OtherRoute

from trips.schema import PointAdd, DriverAdd, PassengerAdd, RouteAdd, CarAdd, CarFuelAdd, PositionAdd, PeopleAdd
from trips.schema import FuelAdd, WhereDriveAdd, RefuelingAdd, OrganizationAdd, OtherRouteAdd
from trips.schema import OrganizationUpdate, PointUpdate, RouteUpdate

from trips.schema import FullPoint, FullRefueling, FullPeople, FullCar, FullFuel, FullCarFuel, FullRoute
from trips.schema import FullWhereDrive, FullDriver, FullPassenger, FullPosition, FullOrganization, FullOtherRoute

from trips.schema import FullRouteRe, FullRefuelingRe, FullFuelRe, FullWhereDriveRe, FullPositionRe, FullOtherRouteRe
from trips.schema import FullCarRe, FullPeopleRe, FullPointRe, FullDriverRe, NamePoint, FullOrganizationRe
from trips.schema import FullPassengerRe, FullPassengerDriverRe, FullOtherRouteDriverRe

import requests
from geopy.geocoders import Nominatim


class UtilityFunction:
    SALT = SALT

    @staticmethod
    def hash_password(self, password: str):
        password = f"{self.SALT}{password}"
        password = password.encode()
        password = md5(password).hexdigest()
        return password

    @staticmethod
    def my_round(num):
        return num if num % 5 == 0 else num + (5 - (num % 5))

    @staticmethod
    def get_geo_point(name):
        loc = Nominatim(user_agent="GetLoc")
        get_location = loc.geocode(name)
        return get_location

    @staticmethod
    def ppr(date_from, date_to, card_number=None, data_format='json'):
        url = r'https://online.petrolplus.ru/api/public-api/v2'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': PPR
        }

        data = {'dateFrom': date_from, 'dateTo': date_to, 'format': data_format}
        if card_number is None:
            res = requests.get(f'{url}/transactions', data, headers=headers).json()
        else:
            res = requests.get(f'{url}/cards/{card_number}/transactions', data, headers=headers).json()
        return res['transactions']

    @staticmethod
    async def get_id_people(ppr_card):
        async with Session() as session:
            query = select(People.id_people).filter(People.ppr_card == ppr_card)
            result = await session.execute(query)
            id_people = result.unique().scalars().first()
            return id_people

    @staticmethod
    async def get_id_fuel(name_fuel):
        async with Session() as session:
            query = select(Fuel.id_fuel).filter(Fuel.name_fuel == name_fuel)
            result = await session.execute(query)
            id_fuel = result.unique().scalars().first()
            return id_fuel

    @staticmethod
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

    @staticmethod
    async def get_id(list_id: list) -> int:
        return max(list_id) + 1 if len(list_id) != 0 else 1

    @staticmethod
    async def get_geo(data: RouteAdd) -> list:
        list_geo = []
        async with Session() as session:
            query_start_point = (
                select(Point)
                .filter(Point.id_point == data.id_start_point)
            )
            result_qsp = await session.execute(query_start_point)
            qsp_models = result_qsp.unique().scalars().all()
            list_geo.append([qsp_models[0].longitude, qsp_models[0].latitude])

            query_finish_point = (
                select(Point)
                .filter(Point.id_point == data.id_finish_point)
            )
            result_qfp = await session.execute(query_finish_point)
            qfp_models = result_qfp.unique().scalars().all()
            list_geo.append([qfp_models[0].longitude, qfp_models[0].latitude])
            return list_geo

    @staticmethod
    async def check_double_route(data: RouteAdd) -> bool:
        async with Session() as session:
            a, b = data.id_start_point, data.id_finish_point
            one = await session.execute(select(Route).filter(Route.id_start_point == int(a),
                                                             Route.id_finish_point == int(b)))
            one_way = one.unique().scalars().first()
            two = await session.execute(select(Route).filter(Route.id_start_point == int(b),
                                                             Route.id_finish_point == int(a)))
            other_way = two.unique().scalars().first()
            if one_way is None and other_way is None:
                return True
            else:
                return False

    @staticmethod
    async def get_route_length(trip: list) -> int:
        async with Session() as session:
            id_trip = []
            for i in range(len(trip) - 1):
                a, b = trip[i], trip[i + 1]
                query = await session.execute(
                    select(Route)
                    .filter(Route.id_start_point == int(a), Route.id_finish_point == int(b))
                )
                one_way = query.unique().scalars().first()
                query = await session.execute(
                    select(Route)
                    .filter(Route.id_start_point == int(b), Route.id_finish_point == int(a))
                )
                other_way = query.unique().scalars().first()
                if one_way is None:
                    id_trip.append(other_way.id_route)
                else:
                    id_trip.append(one_way.id_route)
            query = (await session.execute(select(Route))).unique().scalars().all()
            return sum([i.distance for i in query if i.id_route in id_trip])

    @staticmethod
    async def get_name_point(data: RouteAdd):
        async with Session() as session:
            query = (
                select(Point)
                .filter(or_(Point.id_point == data.id_start_point, Point.id_point == data.id_finish_point))
            )
            result = await session.execute(query)
            models = result.unique().scalars().all()
            return models

    @staticmethod
    async def get_id_point_of_driver(id_driver: int) -> int:
        async with Session() as session:
            query = select(Driver.id_people).filter(Driver.id_driver == id_driver)
            result = await session.execute(query)
            model = result.unique().scalars().first()
            query = select(People.id_point).filter(People.id_people == model)
            result = await session.execute(query)
            id_point_driver = result.unique().scalars().first()
            return id_point_driver

    @staticmethod
    async def get_id_point_factory() -> int:
        async with Session() as session:
            query = select(Point.id_point).filter(Point.name_point == 'Завод')
            result = await session.execute(query)
            id_point_factory = result.unique().scalars().first()
            return id_point_factory

    @staticmethod
    async def check_name_point(name: str) -> bool:
        async with Session() as session:
            query = (
                select(Point.name_point)
                .filter(Point.name_point == name)
            )
            result = await session.execute(query)
            models = result.unique().scalars().all()
            if models:
                return True
            return False

    @staticmethod
    async def build_forward(driver, factory, dto_pas, dto_or) -> list:
        id_point_forward = [driver]
        id_point_forward.extend([i.people.id_point for i in dto_pas if i.where_drive == 1])
        id_point_forward.append(factory)
        id_point_forward.extend([i.organization.id_point for i in dto_or if i.where_drive == 3])
        return id_point_forward

    @staticmethod
    async def build_away(driver, factory, dto_pas, dto_or) -> list:
        id_point_away = []
        id_point_away.extend([i.organization.id_point for i in dto_or if i.where_drive == 4])
        id_point_away.append(factory)
        id_point_away.extend([i.people.id_point for i in dto_pas if i.where_drive == 2])
        id_point_away.append(driver)
        return id_point_away

    @staticmethod
    async def find_distance_of_driver(id_driver):
        async with Session() as session:
            query_passenger = (
                select(Passenger)
                .options(joinedload(Passenger.people))
                .options(joinedload(Passenger.driver))
                .filter(Passenger.id_driver == id_driver)
                .limit(100)
                .order_by(Passenger.order.asc())
            )
            result_pas = await session.execute(query_passenger)
            models_pas = result_pas.unique().scalars().all()
            dto_pas = [FullPassengerDriverRe.model_validate(row, from_attributes=True) for row in models_pas]
            query_or = (
                select(OtherRoute)
                .options(joinedload(OtherRoute.organization))
                .options(joinedload(OtherRoute.driver))
                .filter(OtherRoute.id_driver == id_driver)
                .limit(100)
                .order_by(OtherRoute.order.asc())
            )
            result_or = await session.execute(query_or)
            models_or = result_or.unique().scalars().all()
            dto_or = [FullOtherRouteDriverRe.model_validate(row, from_attributes=True) for row in models_or]
            point_driver = await UtilityFunction.get_id_point_of_driver(id_driver)
            point_factory = await UtilityFunction.get_id_point_factory()
            query_driver = (
                select(Driver.where_drive)
                .filter(Driver.id_driver == id_driver)
            )
            result_driver = await session.execute(query_driver)
            models_driver = result_driver.unique().scalars().all()
            if models_driver[0] == 1:
                point_forward = await UtilityFunction.build_forward(point_driver, point_factory, dto_pas, dto_or)
                point_away = []
            elif models_driver[0] == 2:
                point_forward = []
                point_away = await UtilityFunction.build_away(point_driver, point_factory, dto_pas, dto_or)
            else:
                point_forward = await UtilityFunction.build_forward(point_driver, point_factory, dto_pas, dto_or)
                point_away = await UtilityFunction.build_away(point_driver, point_factory, dto_pas, dto_or)
            length_route_forward = await UtilityFunction.get_route_length(point_forward)
            length_route_away = await UtilityFunction.get_route_length(point_away)
            return dto_pas, dto_or, length_route_forward, point_forward, length_route_away, point_away

    @classmethod
    async def get_route_of_driver(cls, id_people):
        list_route = []
        dict_point = await DataGet.all_name_point()
        async with Session() as session:
            query = select(Driver.id_driver).filter(Driver.id_people == id_people)
            result = await session.execute(query)
            models = result.scalars().all()
        for i in models:
            info = await UtilityFunction.find_distance_of_driver(i)
            list_route.append(map(x: info[3]))
        return list_route

class DataPatch:
    @classmethod
    async def update_point(cls, id_point: int, data: PointUpdate):
        if data.name_point is not None and data.name_point != 'Завод':
            get_location = UtilityFunction.get_geo_point(data.name_point)
            if get_location is None:
                raise HTTPException(status_code=422, detail='Для заднного названия нет геоданных')
            geo_data = {'latitude': get_location.latitude, 'longitude': get_location.longitude}
        else:
            if data.name_point == 'Завод':
                geo_data = {'latitude': 53.389813, 'longitude': 50.431804}
            else:
                geo_data = {}
        async with Session() as session:
            query = (
                update(Point)
                .where(Point.id_point == id_point)
                .values(**(data.model_dump(exclude_none=True)), **geo_data)
                .returning(Point.id_point, Point.name_point, Point.cost, Point.latitude, Point.longitude)
            )
            result = await session.execute(query)
            update_point = result.fetchone()
            await session.commit()
            if update_point is not None:
                return (f'Изменения для id {update_point[0]}: '
                        f'Название - {update_point[1]}, '
                        f'Стоимость - {update_point[2]}, '
                        f'Координаты - [{update_point[3]}: {update_point[4]}]')

    @classmethod
    async def update_organization(cls, id_organization: int, data: OrganizationUpdate):
        async with Session() as session:
            query = (
                update(Organization)
                .where(Organization.id_organization == id_organization)
                .values(**(data.model_dump(exclude_none=True)))
                .returning(Organization.id_organization, Organization.name_organization, Organization.id_point)
            )
            result = await session.execute(query)
            update_organization = result.fetchone()
            await session.commit()
            if update_organization is not None:
                return (f'Изменения для id {update_organization[0]}: '
                        f'Название - {update_organization[1]}, '
                        f'id адреса - {update_organization[2]}')

    @classmethod
    async def update_route(cls, id_route: int, data: RouteUpdate):
        async with Session() as session:
            query = (
                update(Route)
                .where(Route.id_route == id_route)
                .values(**(data.model_dump(exclude_none=True)))
                .returning(Route.id_route, Route.id_start_point, Route.id_finish_point, Route.distance)
            )
            result = await session.execute(query)
            update_route = result.fetchone()
            await session.commit()
            name_route = await UtilityFunction.get_name_point(update_route)
            if update_route is not None:
                return (f'Изменения для id {update_route[0]}: ',
                        f'У маршрута: {name_route[0].name_point} -  {name_route[1].name_point} изменилось растояние',
                        f'Новое значение: {update_route[3]} км')


class DataLoads:
    @classmethod
    async def add_point(cls, data: PointAdd) -> dict:
        get_location = UtilityFunction.get_geo_point(data.name_point)
        if get_location is None:
            raise HTTPException(status_code=422, detail='Для заднного названия нет геоданных')
        async with Session() as session:
            query = select(Point.id_point)
            result = await session.execute(query)
            models = result.unique().scalars().all()
            point = Point(**(data.model_dump()), latitude=get_location.latitude, longitude=get_location.longitude,
                          id_point=await UtilityFunction.get_id(models))
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
        if data.distance is None:
            geo_route = await UtilityFunction.get_geo(data)
            dist = UtilityFunction.my_round(int(UtilityFunction.matrix(geo_route) / 1000))
        else:
            dist = data.distance
        data.distance = dist
        async with Session() as session:
            query = select(Route.id_route)
            result = await session.execute(query)
            models = result.unique().scalars().all()
            route = Route(**(data.model_dump()), id_route=await UtilityFunction.get_id(models))
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
            query = select(Fuel.id_fuel)
            result = await session.execute(query)
            models = result.unique().scalars().all()
            fuel = Fuel(**(data.model_dump()), id_fuel=await UtilityFunction.get_id(models))
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
            query = select(Car.id_car)
            result = await session.execute(query)
            models = result.unique().scalars().all()
            car = Car(**(data.model_dump()), id_car=await UtilityFunction.get_id(models))
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
            query = select(CarFuel.id_car_fuel)
            result = await session.execute(query)
            models = result.unique().scalars().all()
            car_fuel = CarFuel(**(data.model_dump()), id_car_fuel=await UtilityFunction.get_id(models))
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
            query = select(Position.id_position)
            result = await session.execute(query)
            models = result.unique().scalars().all()
            position = Position(**(data.model_dump()), id_position=await UtilityFunction.get_id(models))
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
            query = select(WhereDrive.id_wd)
            result = await session.execute(query)
            models = result.unique().scalars().all()
            wd = WhereDrive(**(data.model_dump()), id_wd=await UtilityFunction.get_id(models))
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
            query = select(People.id_people)
            result = await session.execute(query)
            models = result.unique().scalars().all()
            people = People(**(data.model_dump()), id_people=await UtilityFunction.get_id(models))
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
                "ppr_card": people.ppr_card
            }

    @classmethod
    async def add_organization(cls, data: OrganizationAdd) -> dict:
        async with Session() as session:
            query = select(Organization.id_organization)
            result = await session.execute(query)
            models = result.unique().scalars().all()
            organization = Organization(**(data.model_dump()), id_organization=await UtilityFunction.get_id(models))
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
            query = select(Driver.id_driver)
            result = await session.execute(query)
            models = result.unique().scalars().all()
            driver = Driver(**(data.model_dump()), id_driver=await UtilityFunction.get_id(models))
            session.add(driver)
            await session.flush()
            await session.commit()
            return {
                "id_driver": driver.id_driver,
                "id_people": driver.id_people,
                "date_trip": driver.date_trip,
                "where_drive": driver.where_drive
            }

    @classmethod
    async def add_passenger(cls, data: PassengerAdd) -> dict:
        async with Session() as session:
            query = select(Passenger.id_passenger)
            result = await session.execute(query)
            models = result.unique().scalars().all()
            passenqer = Passenger(**(data.model_dump()), id_passenger=await UtilityFunction.get_id(models))
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
            query = select(OtherRoute.id_other_route)
            result = await session.execute(query)
            models = result.unique().scalars().all()
            other_route = OtherRoute(**(data.model_dump()), id_other_route=await UtilityFunction.get_id(models))
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
            query = select(Refueling.id_refueling)
            result = await session.execute(query)
            models = result.unique().scalars().all()
            refueling = Refueling(**(data.model_dump()), id_refueling=await UtilityFunction.get_id(models))
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

    @classmethod
    async def add_refueling_auto(cls) -> list:
        date_now = datetime.strftime(datetime.now(), '%Y-%m-%d')
        date_start = datetime.strftime(datetime.today().replace(day=1), '%Y-%m-%d')

        list_new_refueling = []
        async with (Session() as session):
            query = (
                select(Refueling)
                .options(joinedload(Refueling.fuel), joinedload(Refueling.people))
                .filter(Refueling.date_refueling >= datetime.strptime(date_start, '%Y-%m-%d').date())
            )
            result = await session.execute(query)
            models = result.unique().scalars().all()
            dto = [FullRefuelingRe.model_validate(row, from_attributes=True) for row in models]
            ccx = [{
                'id_fuel': i.fuel.name_fuel,
                'id_people': i.people.ppr_card,
                'quantity': i.quantity,
                'date_refueling': f"{str(i.date_refueling)[:19]}"} for i in dto]
            ppr = [{
                'id_fuel': i['serviceName'],
                'id_people': str(i['cardNum']),
                'quantity': i['amount'],
                'date_refueling': f"{i['date'][:10]} {i['date'][11:19]}"} for i in UtilityFunction.ppr(date_start, date_now)]
            for i in ppr:
                if i not in ccx:
                    i['id_fuel'] = await UtilityFunction.get_id_fuel(i['id_fuel'])
                    i['id_people'] = await UtilityFunction.get_id_people(i['id_people'])
                    i['date_refueling'] = datetime.strptime(i['date_refueling'], '%Y-%m-%d %H:%M:%S')
                    list_new_refueling.append(i)
            query = select(Refueling.id_refueling)
            result = await session.execute(query)
            models = result.unique().scalars().all()
            refueling = []
            count_id = await UtilityFunction.get_id(models)
            for i in list_new_refueling:
                refueling.append(Refueling(**(dict(i)), id_refueling=count_id))
                count_id += 1
            session.add_all(refueling)
            await session.flush()
            await session.commit()
            return refueling


class DataGet:
    @staticmethod
    async def all_name_point():
        async with Session() as session:
            query = select(Point)
            result = await session.execute(query)
            models = result.unique().scalars().all()
            dto = [NamePoint.model_validate(row, from_attributes=True) for row in models]
            dict_points = {int(i.id_point):i.name_point for i in dto}
            return dict_points

    @staticmethod
    async def all_point():
        async with Session() as session:
            query = select(Point)
            result = await session.execute(query)
            models = result.unique().scalars().all()
            dto = [FullPoint.model_validate(row, from_attributes=True) for row in models]
            return dto

    @staticmethod
    async def find_all_point():
        async with Session() as session:
            query = select(Point).options(selectinload(Point.peoples))
            result = await session.execute(query)
            models = result.unique().scalars().all()
            dto = [FullPointRe.model_validate(row, from_attributes=True) for row in models]
            return dto

    @staticmethod
    async def find_name_point(name_point: str):
        async with Session() as session:
            query = select(Point).options(selectinload(Point.peoples)).filter(Point.name_point == name_point)
            result = await session.execute(query)
            models = result.unique().scalars().all()
            dto = [FullPointRe.model_validate(row, from_attributes=True) for row in models]
            return dto

    @staticmethod
    async def find_all_route():
        async with Session() as session:
            query = (
                select(Route)
                .options(joinedload(Route.point_start), joinedload(Route.point_finish))
                .limit(10)
            )
            result = await session.execute(query)
            models = result.scalars().all()
            dto = [FullRouteRe.model_validate(row, from_attributes=True) for row in models]
            return dto

    @staticmethod
    async def find_all_fuel():
        async with Session() as session:
            query = (
                select(Fuel)
                .options(selectinload(Fuel.refuelings))
            )
            result = await session.execute(query)
            models = result.unique().scalars().all()
            dto = [FullFuelRe.model_validate(row, from_attributes=True) for row in models]
            return dto

    @staticmethod
    async def find_all_car():
        async with Session() as session:
            query = select(Car).options(joinedload(Car.people))
            result = await session.execute(query)
            models = result.unique().scalars().all()
            dto = [FullCarRe.model_validate(row, from_attributes=True) for row in models]
            return dto


    @staticmethod
    async def find_all_car_fuel():
        async with Session() as session:
            query = select(CarFuel)
            result = await session.execute(query)
            models = result.scalars().all()
            return models

    @staticmethod
    async def find_all_position():
        async with Session() as session:
            query = (
                select(Position)
                .options(selectinload(Position.peoples))
            )
            result = await session.execute(query)
            models = result.scalars().all()
            dto = [FullPositionRe.model_validate(row, from_attributes=True) for row in models]
            return dto

    @staticmethod
    async def find_all_wd():
        async with Session() as session:
            query = (
                select(WhereDrive)
                .options(selectinload(WhereDrive.passengers))
                .options(selectinload(WhereDrive.other_routes))
                .options(selectinload(WhereDrive.drivers))
            )
            result = await session.execute(query)
            models = result.unique().scalars().all()
            dto = [FullWhereDriveRe.model_validate(row, from_attributes=True) for row in models]
            return dto

    @staticmethod
    async def find_all_people():
        async with Session() as session:
            query = (
                select(People)
                .options(joinedload(People.point))
                .options(joinedload(People.position))
                .options(selectinload(People.cars))
                .limit(20)
            )
            result = await session.execute(query)
            models = result.unique().scalars().all()
            dto = [FullPeopleRe.model_validate(row, from_attributes=True) for row in models]
            return dto

    @staticmethod
    async def find_all_organization():
        async with Session() as session:
            query = (
                select(Organization)
                .options(joinedload(Organization.point))
            )
            result = await session.execute(query)
            models = result.unique().scalars().all()
            dto = [FullOrganizationRe.model_validate(row, from_attributes=True) for row in models]
            return dto

    @staticmethod
    async def find_user(user_id: int):
        async with Session() as session:
            query = (
                select(People)
                .options(joinedload(People.point))
                .options(joinedload(People.position))
                .options(selectinload(People.cars))
                .filter(People.id_people == user_id)
            )
            result = await session.execute(query)
            models = result.unique().scalars().all()
            dto = [FullPeopleRe.model_validate(row, from_attributes=True) for row in models]
            return dto

    @staticmethod
    async def find_all_driver():
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
            models = result.unique().scalars().all()
            dto = [FullPeopleRe.model_validate(row, from_attributes=True) for row in models]
            return dto


    @staticmethod
    async def find_driver_of_date(now_date_trip):
        async with Session() as session:
            query = (
                select(Driver)
                .options(joinedload(Driver.people))
                .options(joinedload(Driver.wd))
                .filter(Driver.date_trip == now_date_trip)
                .limit(100)
            )
            result = await session.execute(query)
            models = result.unique().scalars().all()
            dto = [FullDriverRe.model_validate(row, from_attributes=True) for row in models]
            return dto

    @staticmethod
    async def find_all_car_carrier():
        async with Session() as session:
            query = (
                select(Driver)
                .options(joinedload(Driver.people))
                .options(joinedload(Driver.wd))
            )
            result = await session.execute(query)
            models = result.unique().scalars().all()
            dto = [FullDriverRe.model_validate(row, from_attributes=True) for row in models]
            return dto

    @staticmethod
    async def find_all_passengers():
        async with Session() as session:
            query = (
                select(Passenger)
                .options(joinedload(Passenger.people))
                .options(joinedload(Passenger.driver))
                .options(joinedload(Passenger.wd))
            )
            result = await session.execute(query)
            models = result.scalars().all()
            dto = [FullPassengerRe.model_validate(row, from_attributes=True) for row in models]
            return dto

    @staticmethod
    async def find_all_other_route():
        async with Session() as session:
            query = (
                select(OtherRoute)
                .options(joinedload(OtherRoute.organization), joinedload(OtherRoute.driver), joinedload(OtherRoute.wd))
            )
            result = await session.execute(query)
            models = result.scalars().all()
            dto = [FullOtherRouteRe.model_validate(row, from_attributes=True) for row in models]
            return dto

    @staticmethod
    async def find_all_refuelings():
        async with Session() as session:
            query = (
                select(Refueling)
                .options(joinedload(Refueling.fuel), joinedload(Refueling.people))
            )
            result = await session.execute(query)
            models = result.scalars().all()
            dto = [FullRefuelingRe.model_validate(row, from_attributes=True) for row in models]
            return dto

    @staticmethod
    async def count_refueling_to_date(date_start, date_finish) -> float:
        # date_now = datetime.strftime(datetime.now(), '%Y-%m-%d')
        # date_start = datetime.strftime(datetime.today().replace(day=1), '%Y-%m-%d')

        list_new_refueling = []
        async with (Session() as session):
            query = (
                select(Refueling.quantity)
                .filter(and_(Refueling.date_refueling >= datetime.strptime(date_start, '%Y-%m-%d').date(),
                             Refueling.date_refueling <= datetime.strptime(date_finish, '%Y-%m-%d').date()))
            )
            result = await session.execute(query)
            models = result.scalars().all()
            count = sum(models)
            # dto = [FullRefuelingRe.model_validate(row, from_attributes=True) for row in models]
            # ccx = [{
            #     'id_fuel': i.fuel.name_fuel,
            #     'id_people': i.people.ppr_card,
            #     'quantity': i.quantity,
            #     'date_refueling': f"{str(i.date_refueling)[:19]}"} for i in dto]
            # ppr = [{
            #     'id_fuel': i['serviceName'],
            #     'id_people': str(i['cardNum']),
            #     'quantity': i['amount'],
            #     'date_refueling': f"{i['date'][:10]} {i['date'][11:19]}"} for i in
            #     UtilityFunction.ppr(date_start, date_now)]
            # for i in ppr:
            #     if i not in ccx:
            #         i['id_fuel'] = await UtilityFunction.get_id_fuel(i['id_fuel'])
            #         i['id_people'] = await UtilityFunction.get_id_people(i['id_people'])
            #         i['date_refueling'] = datetime.strptime(i['date_refueling'], '%Y-%m-%d %H:%M:%S')
            #         list_new_refueling.append(i)
            # query = select(Refueling.id_refueling)
            # result = await session.execute(query)
            # models = result.unique().scalars().all()
            # refueling = []
            # count_id = await UtilityFunction.get_id(models)
            # for i in list_new_refueling:
            #     refueling.append(Refueling(**(dict(i)), id_refueling=count_id))
            #     count_id += 1
            # session.add_all(refueling)
            # await session.flush()
            # await session.commit()
            return count



