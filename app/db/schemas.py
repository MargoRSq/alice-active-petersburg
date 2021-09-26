from pydantic import BaseModel

from app.db.models import RouteType

class Route(BaseModel):
    name: str
    route_type: RouteType
    distance: float
    fact: str
    url: str

class Weather(BaseModel):
    data: str