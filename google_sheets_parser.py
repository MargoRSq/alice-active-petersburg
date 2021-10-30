import requests

from sys import argv

from app.db.operations import post_one_route

def parse_sheet(url):
    response = requests.get(url)
    json = response.json()

    return json

def post_routes_from_json(json):
    for route in json:
        post_one_route(route_type=route['type'],
                       tags=route['tags'],
                       fact=route['fact'],
                       gaia_route_id=route['route_id'])


routes_json = parse_sheet(argv[1])
post_routes_from_json(routes_json)
