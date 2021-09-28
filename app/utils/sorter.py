from app.db.models import RouteType
from app.db.operations import get_routes


def tags_sort(tags, routes):
    result_dict = {}
    for route in routes:
        for tag in tags:
            if tag in route['tags']:
                route_id = route['id']
                if route_id not in result_dict:
                    result_dict[route_id] = {'route': route, 'count': 1}
                else:
                    result_dict[route_id]['count'] += 1
    sorted_dict = dict(reversed(sorted(result_dict.items(), key=lambda item: item[1]['count'])))
    sorted_routes = [route_dict[1]['route'] for route_dict in sorted_dict.items()]
                
    return sorted_routes

def filter_routes(distance: float, tags: str, 
                  route_type: RouteType = RouteType.running.value) -> list[dict]:
    all_routes = get_routes(route_type=route_type, distance=distance)
    tags_list = tags.split(',')
    tags_routes = tags_sort(tags_list, all_routes)

    return tags_routes
