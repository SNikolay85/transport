from contextlib import asynccontextmanager
import uvicorn

from fastapi import FastAPI

from trips.models_temp import delete_tables, create_tables
from trips.router import router_point as point, router_route as route, router_car as car
from trips.router import router_car_fuel as car_fuel, router_people as people, router_position as position
from trips.router import router_driver as driver, router_passenger as passenger


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     await delete_tables()
#     print('База очищена')
#     await create_tables()
#     print('База создана заново')
#     yield
#     print('Выключение')


#app_route = FastAPI(lifespan=lifespan)
app_route = FastAPI(title='Transport')
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