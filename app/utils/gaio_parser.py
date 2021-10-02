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


def build_plot(distance: float, elevation: list[int], mn: int):
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
    im2 = Image.open('img/orig.png').resize((28*mn, 28*mn))

    im1.paste(im2, (4*mn, 4*mn))

    result_image = BytesIO()
    im1.save(result_image, format='PNG')
    
    return result_image

from time import time
from pprint import pprint

start = time()
json = get_gaia_route_json('34250d75-844c-4b45-ae76-872459ac9ad0')

# pprint(json)

# print(time() - start)

def get_route_info(route_json: dict):
    route_info = {}
    
    route = route_json['features']
    properties = route[0]['properties']

    coordinates = route[0]['geometry']['coordinates'][0]
    coordinates_array = [(coordinates[i][0], coordinates[i][1])
                         for i in range(len(coordinates))]
    
    route_info['points'] = [{'long': coordinates_array[i][0], 'lat': coordinates_array[i][1]}
                         for i in range(len(coordinates_array))]
    route_info['name'] = properties['title']
    route_info['distance'] = round((properties['distance'] / 1000), 2)
    route_info['elevation_array'] = [point['properties']['elevation'] for point in route[1:]]
    route_info['elevation_result'] = route_info['elevation_array'][0] - route_info['elevation_array'][-1]

    return route_info

# pprint(get_route_info(json))
