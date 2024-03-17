from contextlib import asynccontextmanager

from fastapi import FastAPI

from trips.database import delete_tables, create_tables
from trips.router import router as tasks_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    print('База очищена')
    await create_tables()
    print('База создана заново')
    yield
    print('Выключение')


app_route = FastAPI(lifespan=lifespan)
app_route.include_router(tasks_router)









# class Users(BaseModel):
#     name: str
#     email: str
#     age: int
#     is_subscribed: bool
#
# @trips.post('/create_user')
# async def create(user: Users):
#     return {
#         "name": user.name,
#         "email": user.email,
#         "age": user.age,
#         "is_subscribed": user.is_subscribed
#     }

# @trips.get('/product/{product_id}')
# async def search_user(product_id: int):
#     for k, i in enumerate(sample_products):
#         if product_id == i['product_id']:
#             return sample_products[k]
#     return {"error": "User not found"}



