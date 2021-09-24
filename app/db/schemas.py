from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

from app.db.models import RouteType

class Route(BaseModel):
    type: RouteType
    distance: float
    fact: str
    url: str