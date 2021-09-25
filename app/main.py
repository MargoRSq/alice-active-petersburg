from fastapi import FastAPI
from fastapi import FastAPI, Depends
from typing import List

from app.db.schemas import Route, Weather
from app.db.models import RouteType
from app.utils.weather import get_weather
# from app.utils.gsheets_parser import parse_table

app = FastAPI(title='active-petersburg', version='1.0.0')

async def common_parameters(distance: float, tags: str, type: RouteType = RouteType.running.value):
    return {"type": type, "distance": distance, "tags": tags}

@app.get('/routes', response_model=List[Route])
async def fetch_routes(commons: dict = Depends(common_parameters)):
    one_route = {
    'type': 'wheel', 
    'distance': 3.9, 
    'fact': 'lol',
    'url': ''}
    routes = [one_route, one_route, one_route, one_route]
    return routes 

@app.get('/weather', response_model=Weather)
async def fetch_weather():
    return {"data": get_weather()}
