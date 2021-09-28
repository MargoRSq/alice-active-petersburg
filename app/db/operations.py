from sqlalchemy import select, insert, delete

from app.db.models import Routes, RouteType
from app.db.db import Base, engine, session
from app.utils.gaio_parser import get_elevation


def check_route(url: str):
    q = session.query(Routes).filter(Routes.url == url)
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
    select_state = (
        select(Routes).
        where(Routes.route_type == route_type, Routes.distance <= distance)
    )
    with engine.connect() as conn:
        result = conn.execute(select_state)
    return [dict(route)for route in result.fetchall()]

def post_routes(name, route_type, distance, tags, fact, url, route_id_gaio):
    elevation_array = get_elevation(route_id_gaio)
    elevation_result = elevation_array[0] - elevation_array[-1]
    if not check_route(url):
        insert_state = (
            insert(Routes).
            values(name=name ,route_type=route_type, 
                   distance=distance, tags=tags, fact=fact, url=url,
                   elevation_array=elevation_array, elevation_result=elevation_result,
                   route_id=route_id_gaio))
        with engine.connect() as conn:
            conn.execute(insert_state)

gaio_id = '34250d75-844c-4b45-ae76-872459ac9ad0'
url = 'https://yandex.ru/maps/213/moscow/?ll=37.622285%2C55.750077&mode=routes&rtext=55.730826%2C37.598034~55.738865%2C37.610737~55.756104%2C37.604904&rtt=pd&ruri=~~&z=10'
post_routes('hello','running', 3.9, 'адмиралтийский,набережная,парк', 'рофлофакт', url+'1', route_id_gaio=gaio_id)
post_routes('hello','wheel', 3.9, 'адмиралтийский,набережная,парк', 'рофлофакт', url+'2', route_id_gaio=gaio_id)
post_routes('hello','wheel', 4.5, 'парк,победа', 'рофлофакт', url+'3', route_id_gaio=gaio_id)
post_routes('hello','running', 3.9, 'адмиралтийский', 'рофлофакт', url+'7', route_id_gaio=gaio_id)
post_routes('hello','running', 3.9, 'адмиралтийский,набережная,парк,набережная,адмиралтийский,адмиралтийский', 'рофлофакт', url+'6', route_id_gaio=gaio_id)