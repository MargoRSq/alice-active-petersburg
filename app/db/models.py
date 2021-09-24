import enum

from sqlalchemy import Column, Integer, String, Enum, BigInteger, Float

from app.db.db import engine, Base


class RouteType(enum.Enum):
    running = 'running'
    wheel = 'wheel'

class Routes(Base):
    __tablename__ = 'routes_table'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    route_type = Column(Enum(RouteType))
    distance = Column(Float)
    tags = Column(String(100))
    fact = Column(String(100))
    url = Column(String(1000))

Base.metadata.create_all(engine)
