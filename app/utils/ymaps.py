from app.db.models import RouteType

def queris_map_creator(coordinates: list, route_type: RouteType) -> str:
    result_query = 'rtext='
    start_long = coordinates[0]['long']
    start_lat = coordinates[0]['lat']
    result_query += f"{start_lat},{start_long}"
    for point in coordinates[1:]:
        long = point['long']
        lat = point['lat']
        result_query += f"~{lat},{long}"

    if route_type == RouteType.pedestrian or route_type == RouteType.running:
        result_query+="&rtt=pd"
    elif route_type == RouteType.wheel:
        result_query+="&rtt=bc"

    return result_query


def queries_image_creator(coordinates: list):

    result_query = ''
    start_long = coordinates[0]['long']
    start_lat = coordinates[0]['lat']
    result_query += f'&pt={start_long},{start_lat},ya_ru'

    end_long = coordinates[-1]['long']
    end_lat = coordinates[-1]['lat']
    result_query += f"~{end_long},{end_lat},flag"

    result_query += "&pl="
    for point in coordinates:
        long = point['long']
        lat = point['lat']
        result_query += f"{long},{lat},"

    return result_query
