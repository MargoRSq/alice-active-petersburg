from fastapi import FastAPI
from typing import List

from app.db.schemas import Route

app = FastAPI(title='active-petersburg', version='1.0.0')

@app.get('/routes', response_model=List[Route])
def get_routes(str: str): 
    one_route = {
    'type': 'wheel', 
    'distance': 3.9, 
    'fact': 'lol',
    'url': ''}
    routes = [one_route]
    return routes