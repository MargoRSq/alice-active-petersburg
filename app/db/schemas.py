from pydantic import BaseModel

from db.models import RouteType

class Route(BaseModel):
    id: int
    name: str
    route_type: RouteType
    distance: float
    fact: str
    url: str
    elevation_result: int
    elevation_image: str

class Weather(BaseModel):
    data: str