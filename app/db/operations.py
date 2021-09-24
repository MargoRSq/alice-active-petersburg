from sqlalchemy import select, insert, delete

from app.db.models import Routes, RouteType
from app.db.db import engine, session


def check_route(url: str):
    q = session.query(Routes).filter(Routes.url == url)
    return session.query(q.exists()).scalar()


def get_routes(route_type: RouteType, distance: float):
    select_state = (
        select(Routes).
        where(Routes.route_type == route_type, Routes.distance <= distance)
    )
    with engine.connect() as conn:
        result = conn.execute(select_state)
    return result.fetchall()

def post_routes(route_type, distance, tags, fact, url):
    if not check_route(url):
        insert_state = (
            insert(Routes).
            values(route_type=route_type, distance=distance, tags=tags, fact=fact, url=url))
        with engine.connect() as conn:
            conn.execute(insert_state)
