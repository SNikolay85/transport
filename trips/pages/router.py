from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router_page = APIRouter(
    prefix='/pages',
    tags=['Pages']
)

templates = Jinja2Templates(directory='trips/templates')

@router_page.get('/base')
def get_base_page(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})

@router_page.get('/image')
def get_image_page(request: Request):
    return templates.TemplateResponse('image_f.html', {'request': request})