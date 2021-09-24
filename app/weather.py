import requests

from pprint import pprint
from utils.config import YW_TOKEN

headers = {'X-Yandex-API-Key': YW_TOKEN}

url = 'https://api.weather.yandex.ru/v2/forecast?lat=59.9311&lon=30.3609&lang=ru&limit=1'

r = requests.get(url, headers=headers)

tags = ['condition', 'feels_like', 'season', 'wind_speed', 'sunset']


pprint(r.json())
