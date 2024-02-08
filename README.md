# Объявления

### Запуск контейнера выполнить командой: 
*docker-compose up -d*

### Запуск приложения: 
*python server.py*

### Отправка запросов через REST Client или Postman: 

Примеры запросов можно взять из ***requests-examples.http***:

@baseUrl = http://localhost:8000/advertisements

```
# просмотр объявления
GET {{baseUrl}}/1
Content-Type: application/json
```
```
# создание объявления
POST {{baseUrl}}/
Content-Type: application/json

{
  "header": "adv_1", 
  "description": "text_1", 
  "user": "user_1"
}
```
```
# обновление объявления
PATCH {{baseUrl}}/user_1/1
Content-Type: application/json

{
    "header": "adv_2",
    "description": "text_2",
    "user": "user_1"
}
```
```
# удаление объявления
DELETE {{baseUrl}}/user_1/1
Content-Type: application/json
```