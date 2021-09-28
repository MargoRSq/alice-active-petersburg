import requests
import math

import matplotlib.pyplot as plt
import numpy as np

from PIL import Image
from io import BytesIO


def get_elevation(route_id: str):
    url = f'https://www.gaiagps.com/api/objects/track/{route_id}/'
    resp_json = requests.get(url).json()
    return [point['properties']['elevation'] for point in resp_json['features'][1:]]


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
    fig.set_size_inches(382*mn*px, 172*mn*px)
    fig.savefig(plot_file)

    im1 = Image.open(plot_file)
    im2 = Image.open('img/orig.png').resize((28*mn, 28*mn))

    im1.paste(im2, (4*mn, 4*mn))

    result_image = BytesIO()
    im1.save(result_image, format='PNG')
    
    return result_image
