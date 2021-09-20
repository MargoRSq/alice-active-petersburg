import enum

from sqlalchemy import Column, Integer, String, Enum, BigInteger, Float

from db.db import engine, Base


class RouteType(enum.Enum):
    running = 'running'
    wheel = 'wheel'

class Routes(Base):
    __tablename__ = 'routes_table'

    id = Column(Integer, primary_key=True)
    route_type = Column(Enum(RouteType))
    distance = Column(Float)
    tags_place = Column(String(1000))
    tags_route = Column(String(1000))
    fact = Column(String(100))
    url = Column(String(1000))

Base.metadata.create_all(engine)
