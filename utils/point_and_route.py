import requests

from geopy.geocoders import Nominatim
from config import TOKEN_ORS


def my_round(num):
    return num if num % 5 == 0 else num + (5 - (num % 5))


# получение координат по названию
def get_geo_position(name: str):
    loc = Nominatim(user_agent="GetLoc")
    get_loc = loc.geocode(name)
    print(f' Полный адрес: {get_loc.address}')
    return get_loc.latitude, get_loc.longitude


# получение названия по координатам
def get_name_address(geo_position: str):
    loc = Nominatim(user_agent="GetLoc")
    loc_name = loc.reverse(geo_position)
    return loc_name.address


# получение расстояния между точками
def matrix(locations: list):
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'Accept': 'application/json',
        'Authorization': TOKEN_ORS
    }

    data = {"locations":locations,"metrics": ["distance"],"units":"m"}
    res = requests.post(f'https://api.openrouteservice.org/v2/matrix/driving-car',
                        headers=headers,
                        json=data).json()
    return res['distances'][0][1]


def description(address1, address2, la1, lon1, la2, lon2):
    a = f' Для названия: {address1} \n "latitude": {la1}, "longitude": {lon1}'
    b = f' Для названия: {address2} \n "latitude": {la2}, "longitude": {lon2}'
    return print(a), print(b)

# п. Мирный, Нефтянников, 62
name_address_start = 'Завод'
name_address_finish = 'Новосемейкино, Матюгина, 54'

print(get_name_address('53.505223, 50.281860'))

if name_address_start == 'Завод':
    finish_geo_position = get_geo_position(name_address_finish)
    route = [[50.431804, 53.389813], [finish_geo_position[1], finish_geo_position[0]]]
    description('Завод', name_address_finish, route[0][1], route[0][0], route[1][1], route[1][0])
else:
    start_geo_position = get_geo_position(name_address_start)
    finish_geo_position = get_geo_position(name_address_finish)
    route = [[start_geo_position[1], start_geo_position[0]], [finish_geo_position[1], finish_geo_position[0]]]
    description(name_address_start, name_address_finish, route[0][1], route[0][0], route[1][1], route[1][0])

# print(f' Для названия: {name_address_start} \n "latitude": {start_geo_position[0]}, "longitude": {start_geo_position[1]}')
# print(f' Для названия: {name_address_finish} \n "latitude": {finish_geo_position[0]}, "longitude": {finish_geo_position[1]}')


if __name__ == '__main__':
    print(f'Расстояние между {name_address_start} - {name_address_finish}: {my_round(int((matrix(route) / 1000)))} км')
    print(f'Расстояние между {name_address_start} - {name_address_finish}: {(matrix(route) / 1000)} км')

