from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import Response
from typing import List

from db.schemas import Route, Weather
from db.models import RouteType, Routes
from db.operations import get_atr_Routes, post_one_route
from utils.weather import get_weather
from utils.sorter import filter_routes
from utils.gaio_parser import build_plot, get_route_info


app = FastAPI(title='active-petersburg', version='1.0.0')

async def routes_parameters(distance: float, tags: str, type: RouteType = RouteType.running.value):
    return {"type": type, "distance": distance, "tags": tags}

async def posting_parameters(tags: str, fact: str, gaia_id: str,
                             type: RouteType = RouteType.pedestrian.value,):
    return {"type": type, "gaia_id": gaia_id, "tags": tags, "fact": fact} 


@app.get('/routes', response_model=List[Route])
async def fetch_routes(commons: dict = Depends(routes_parameters)):
    return filter_routes(commons['distance'], commons['tags'], commons['type'])

@app.get('/weather', response_model=Weather)
async def fetch_weather():
    return {"data": get_weather()}

@app.get('/elevation_image/{db_id}')
async def fetch_image(db_id: int, mn: int):
    try:
        route = get_atr_Routes(atrs=[Routes.gaia_id, Routes.elevation_array, Routes.distance], id=db_id)
        image_bytes = build_plot(mn=mn, distance=route['distance'], elevation=route['elevation_array'])
        return Response(content=image_bytes.getvalue(), media_type="image/png")
    except BaseException:
        raise HTTPException(status_code=404, detail="route not found")

@app.get('/post_route')
def post_route(commons: dict = Depends(posting_parameters)):
    try:
        post_one_route(commons['type'], commons['tags'], commons['fact'], commons['gaia_id'])
        return {"data": "Маршрут добавлен в базу данных"}
    except BaseException:
        return {"data": "Что-то пошло не так"}

