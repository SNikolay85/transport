from contextlib import asynccontextmanager
import uvicorn

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from trips.router import router_point as point, router_route as route, router_car as car
from trips.router import router_car_fuel as car_fuel, router_people as people, router_position as position
from trips.router import router_driver as driver, router_passenger as passenger


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     redis = aioredis.from_url("redis://localhost", encoding="utf-8", decode_responses=True)
#     FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
#     print('Server started, Redis run')
#     yield
#     print('Выключение')


app_route = FastAPI(title='Transport') #, lifespan=lifespan)
app_route.include_router(point)
app_route.include_router(route)
app_route.include_router(car)
app_route.include_router(car_fuel)
app_route.include_router(position)
app_route.include_router(people)
app_route.include_router(driver)
app_route.include_router(passenger)


# if __name__ == '__main__':
#     uvicorn.run(app_route, host="0.0.0.0", port=8000, log_level="info")

# uvicorn trips.main:app_route --host 0.0.0.0 --port 8000 --reload