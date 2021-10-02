import enum

from sqlalchemy import Column, Integer, String, Enum,  Float

from db.db import engine, Base


class RouteType(enum.Enum):
    running = 'running'
    wheel = 'wheel'
    pedestrian = 'pedestrian'

class Routes(Base):
    __tablename__ = 'routes_table'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    route_type = Column(Enum(RouteType))
    distance = Column(Float)
    tags = Column(String(100))
    fact = Column(String(100))
    ym_url = Column(String(10000))
    gaia_id = Column(String(50))
    elevation_array = Column(String(10000))
    elevation_result = Column(Integer)
    elevation_image = Column(String(100))
    route_image = Column(String(10000))


Base.metadata.create_all(engine)
