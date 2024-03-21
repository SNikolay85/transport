from contextlib import asynccontextmanager
import uvicorn

from fastapi import FastAPI

from trips.models import delete_tables, create_tables
from trips.router import router as trips_router


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
app_route.include_router(trips_router)

# if __name__ == '__main__':
#     uvicorn.run(app_route, host="0.0.0.0", port=8000, log_level="info")

# uvicorn trips.main:app_route --host 0.0.0.0 --port 8000 --reload