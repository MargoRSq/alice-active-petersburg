from fastapi import FastAPI
from typing import List

from db.schemas import Route

app = FastAPI(title='instorify-api', version='1.0.0')

@app.get('/routes', response_model=List[Route])
def get_routes(str: str): 
    one_route = {'id': 1, 'type': 'wheel', 'distance': 3.9, 'tags_place': ['александровский', 'парк'], 'tags_route': ['вода', 'дорожка'], 'url': ''}
    routes = [one_route*5]
    return routes