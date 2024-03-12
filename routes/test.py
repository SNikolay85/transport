from typing import Optional, Annotated

import uvicorn
from fastapi import FastAPI, Depends
from fastapi.responses import FileResponse
from pydantic import BaseModel, ValidationError, Field, field_validator


app_route = FastAPI()


class STasksAdd(BaseModel):
    name: str
    description: Optional[str] = None


class STasks(STasksAdd):
    id: int


tasks = []


@app_route.post('/tasks')
async def add_tasks(task: Annotated[STasksAdd, Depends()]):
    tasks.append(task)
    return {'ok': True}


# @app_route.get('/tasks')
# def get_tasks():
#     task = STasks(id=1, name="first task")
#     return task


# class Users(BaseModel):
#     name: str
#     email: str
#     age: int
#     is_subscribed: bool
#
# @routes.post('/create_user')
# async def create(user: Users):
#     return {
#         "name": user.name,
#         "email": user.email,
#         "age": user.age,
#         "is_subscribed": user.is_subscribed
#     }

# @routes.get('/product/{product_id}')
# async def search_user(product_id: int):
#     for k, i in enumerate(sample_products):
#         if product_id == i['product_id']:
#             return sample_products[k]
#     return {"error": "User not found"}



