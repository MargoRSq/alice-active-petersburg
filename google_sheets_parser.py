import requests

from app.db.operations import post_one_route

def parse_sheet(url: str):
    response = requests.get(url)
    json = response.json()

    return json

def post_routes_from_json(json: dict):
    for route in json:
        post_one_route(route_type=route['type'],
                       tags=route['tags'],
                       fact=route['fact'],
                       gaia_route_id=route['route_id'])


routes_json = parse_sheet('https://opensheet.vercel.app/1Rh9Pzc5lRjQKLddSoVz01ku9jfVdCNpxGkoq3IhZZC4/Sheet1')
post_routes_from_json(routes_json)
