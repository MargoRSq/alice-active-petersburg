from sqlalchemy import select, insert, delete, update

from db.models import Routes, RouteType
from db.db import Base, engine, session
from utils.gaio_parser import get_route_info
from utils.ymaps import queries_image_creator, queris_map_creator


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
    select_state = (
        select(Routes).
        where(Routes.route_type == route_type, Routes.distance <= distance)
    )
    with engine.connect() as conn:
        result = conn.execute(select_state)
    return [dict(route)for route in result.fetchall()]

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
            values(elevation_image=f"https://alice-active-petersburg.herokuapp.com/elevation_image/{id}",
                   route_image=route_img).\
            where(Routes.id == id))
            conn.execute(stmt)


# gaio_id = '34250d75-844c-4b45-ae76-872459ac9ad0'
# url = 'https://yandex.ru/maps/213/moscow/?ll=37.622285%2C55.750077&mode=routes&rtext=55.730826%2C37.598034~55.738865%2C37.610737~55.756104%2C37.604904&rtt=pd&ruri=~~&z=10'
# post_routes('hello','running', 3.9, 'адмиралтийский,набережная,парк', 'рофлофакт', url+'1', route_id_gaio=gaio_id)
# post_routes('hello','wheel', 3.9, 'адмиралтийский,набережная,парк', 'рофлофакт', url+'2', route_id_gaio=gaio_id)
# post_routes('hello','wheel', 4.5, 'парк,победа', 'рофлофакт', url+'3', route_id_gaio=gaio_id)
# post_routes('hello','running', 3.9, 'адмиралтийский', 'рофлофакт', url+'7', route_id_gaio=gaio_id)
# post_routes('hello','running', 3.9, 'адмиралтийский,набережная,парк,набережная,адмиралтийский,адмиралтийский', 'рофлофакт', url+'6', route_id_gaio=gaio_id)

def post_one_route(route_type: RouteType, tags: str, fact: str, gaia_route_id: str):
    gaia_info = get_route_info(gaia_route_id)
    ym_queries = queries_image_creator(gaia_info['points'])

    ym_url = 'https://yandex.ru/maps/?'+ queris_map_creator(gaia_info['points'])

    insert_route(**gaia_info, route_type=route_type, 
                 tags=tags, fact=fact, ym_queries=ym_queries, ym_url=ym_url)


post_one_route('running', 'площадь,парк', 'факт', '34250d75-844c-4b45-ae76-872459ac9ad0')





