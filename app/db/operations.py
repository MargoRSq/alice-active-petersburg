from sys import argv
from sqlalchemy import select, insert, update

from app.db.models import Routes, RouteType
from app.db.db import engine, session
from app.utils.gaio_parser import get_route_info
from app.utils.ymaps import queries_image_creator, queris_map_creator
from app.utils.config import HOST, PORT


def check_route(gaia_id: str):
    q = session.query(Routes).filter(Routes.gaia_id == gaia_id)
    return session.query(q.exists()).scalar()

def get_atr_Routes(atrs, id: int):
    select_state = (
        select(atrs).
        where(Routes.id == id)
    )
    with engine.connect() as conn:
        result = conn.execute(select_state)
    return dict(result.fetchone())


def get_routes(route_type: RouteType, distance: float):
    if distance != 777:
        select_state = (
            select(Routes).
            where(Routes.route_type == route_type, Routes.distance <= distance + 5, Routes.distance >= distance - 5)
        )
    else:
        select_state = (
            select(Routes).
            where(Routes.route_type == route_type, Routes.distance < 777)
        )
    with engine.connect() as conn:
        result = conn.execute(select_state)
        routes = [dict(route)for route in result.fetchall()]
    for route in routes:
        route['elevation_image'] = f"https://{HOST}:{PORT}/elevation_image/{route['id']}?mn=2"
        route['distance'] = round(route['distance'], 1)
    return routes

def insert_route(name, route_type,
                 distance, tags,
                 fact, gaia_id,
                 elevation_array, elevation_result,
                 ym_queries, ym_url,
                 *args, **kwargs):
    if not check_route(gaia_id):
        insert_state = (
            insert(Routes).returning(Routes.id).
            values(name=name ,route_type=route_type, ym_url=ym_url,
                   distance=distance, tags=tags, fact=fact, gaia_id=gaia_id,
                   elevation_array=elevation_array, elevation_result=elevation_result))
        with engine.connect() as conn:
            result = conn.execute(insert_state)
            id = result.fetchone()[0]
            route_img = f"https://static-maps.yandex.ru/1.x/?l=map{ym_queries}"[:-1]
            stmt = (update(Routes).
            values(route_image=route_img).\
            where(Routes.id == id))
            conn.execute(stmt)


def post_one_route(route_type: RouteType, tags: str, fact: str, gaia_route_id: str):
    gaia_info = get_route_info(gaia_route_id)
    ym_queries = queries_image_creator(gaia_info['points'])

    ym_url = 'https://yandex.ru/maps/?'+ queris_map_creator(gaia_info['points'], route_type)

    insert_route(**gaia_info, route_type=route_type,
                 tags=tags, fact=fact, ym_queries=ym_queries, ym_url=ym_url)
