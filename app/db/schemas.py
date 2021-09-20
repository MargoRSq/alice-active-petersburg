from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

from db.models import RouteType

class Route(BaseModel):
    id: int
    distance: float
    fact: str
    url: str