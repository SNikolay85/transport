from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from trips.reposit import DataGet

router_page = APIRouter(
    prefix='/pages',
    tags=['Pages']
)

templates = Jinja2Templates(directory='trips/templates')


@router_page.get('/index')
def get_base_index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@router_page.get('/example')
def get_base_page(request: Request):
    return templates.TemplateResponse('example.html', {'request': request})


@router_page.get('/base')
def get_base_page(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@router_page.get('/trip')
def get_trip_page(request: Request, points=Depends(DataGet.find_all_point)):
    return templates.TemplateResponse('trip.html', {'request': request, 'points': points})


@router_page.get('/add_base')
def get_add_base(request: Request, points=Depends(DataGet.all_point)):
    return templates.TemplateResponse('add_data.html', {'request': request, 'points': points})
