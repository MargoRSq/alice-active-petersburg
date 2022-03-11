import requests
import math

import matplotlib.pyplot as plt
import numpy as np

from PIL import Image
from io import BytesIO
from functools import lru_cache


@lru_cache(maxsize=100)
def get_gaia_route_json(route_id: str):
    url = f'https://www.gaiagps.com/api/objects/track/{route_id}/'
    return requests.get(url).json()


def get_elevation(route_id: str):
    return [point['properties']['elevation']
            for point in get_gaia_route_json(route_id)['features'][1:]]


def build_plot(distance: float, elevation, mn: int):
    plt.rcParams.update({'font.size': 4 if mn == 1 else math.log(600**mn, 7)})
    elevation_list = list(map(int, elevation[1:-1].split(',')))

    rounded = round(distance, 2)
    if distance - rounded < 0.5:
        distance = math.ceil(distance)
    else:
        distance = int(distance)
    step = distance/len(elevation_list)
    dist = np.arange(0.0, distance, step)
    elevation = np.array(elevation_list)
    np.array()

    fig, ax = plt.subplots()
    ax.plot(dist, elevation, color='purple')
    ax.set(xlabel='Дистанция (км)', ylabel='Перепады (м)',
        title='График перепада высот')
    ax.grid()

    plot_file = BytesIO()
    px = 1/plt.rcParams['figure.dpi']
    fig.set_size_inches(382*round(mn)*px, 172*round(mn)*px)
    fig.savefig(plot_file)

    im1 = Image.open(plot_file)
    im2 = Image.open('app/img/orig.png').resize((28*mn, 28*mn))

    im1.paste(im2, (4*mn, 4*mn))

    result_image = BytesIO()
    im1.save(result_image, format='PNG')

    return result_image

def get_route_info(route_id: str):
    route_info = {}

    route_json = get_gaia_route_json(route_id)
    route = route_json['features']
    properties = route[0]['properties']
    points = {point['properties']['order']: point['properties'] for point in route[1:]}
    points = {k: v for k, v in sorted(points.items(), key=lambda item: item[0])}

    route_info['gaia_id'] = route_id
    route_info['points'] = [{'long': point[1]['longitude'], 'lat': point[1]['latitude']}
                         for point in list(points.items())]
    route_info['name'] = properties['title']
    route_info['distance'] = round((properties['distance'] / 1000), 2)
    route_info['elevation_array'] = [point['properties']['elevation'] for point in route[1:]]
    route_info['elevation_result'] = route_info['elevation_array'][0] - route_info['elevation_array'][-1]

    return route_info
