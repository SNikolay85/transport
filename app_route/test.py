import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, ValidationError, Field, field_validator


app_route = FastAPI()

class User(BaseModel):
    name: str
    age: int


# external_data = {
#     "name": "John",
#     "id": 1
# }
# # имитируем распаковку входящих данных в коде приложения
# user = User(**external_data)
user = User(name="Johhhhn", age=10)


@app_route.post('/user')
async def users_age():
    if user.age >= 18:
        return {"name": user.name, "age": user.age, "rt": "true"}
    else:
        return {"name": user.name, "age": user.age, "rt": "false"}

@app_route.get('/')
async def root():
    return FileResponse('website/index.html')


@app_route.post('/calculate')
async def calculate(num1=15, num2=10):
    return f'result = {num1 + num2}'


# if __name__ == '__main__':
#     uvicorn.run(app,
#                 host='127.0.0.1',
#                 port=8000)
