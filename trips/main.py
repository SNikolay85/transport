from contextlib import asynccontextmanager
import uvicorn

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from trips.router import router_point as point, router_route as route, router_car as car
from trips.router import router_car_fuel as car_fuel, router_people as people, router_position as position
from trips.router import router_driver as driver, router_passenger as passenger, router_refueling as refueling
from trips.router import router_fuel as fuel, router_wd as wd, router_organization as organization
from trips.router import router_other_route as other_route

from trips.pages.router import router_page
#SALT=djjfjj53jjd@djdjd

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url("redis://localhost", encoding="utf-8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    print('Server started, Redis run')
    yield
    print('Выключение')


app_route = FastAPI(title='Transport', lifespan=lifespan)

app_route.mount('/trips/static/image', StaticFiles(directory='trips/static/image'), name='static')
app_route.mount('/trips/static/css', StaticFiles(directory='trips/static/css'), name='css')

app_route.include_router(point)
app_route.include_router(route)
app_route.include_router(car)
app_route.include_router(fuel)
app_route.include_router(wd)
app_route.include_router(car_fuel)
app_route.include_router(position)
app_route.include_router(people)
app_route.include_router(organization)
app_route.include_router(driver)
app_route.include_router(passenger)
app_route.include_router(other_route)
app_route.include_router(refueling)
app_route.include_router(router_page)

origins = [
    'http://localhost:8000',
    'http://localhost:8001',
    'http://127.0.0.1:8000',
    'http://127.0.0.1:8001',
]

app_route.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"],
    allow_headers=["Set-Cookie", "Access-Control-Allow-Headers", "Authorization", "Accept", "Accept-Language", "Content-Language", "Content-Type"],
)


# if __name__ == '__main__':
#     uvicorn.run(app_route, host="0.0.0.0", port=8000, log_level="info")

# uvicorn trips.main:app_route --host 0.0.0.0 --port 8000 --reload