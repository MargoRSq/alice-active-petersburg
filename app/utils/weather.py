import requests

from app.utils.config import YW_TOKEN

headers = {'X-Yandex-API-Key': YW_TOKEN}
url = 'https://api.weather.yandex.ru/v2/forecast?lat=59.9311&lon=30.3609&lang=ru&limit=1'

def get_weather():
    r = requests.get(url, headers=headers)
    json = r.json()
    condition = json['fact']['condition']
    feels_like = json['fact']['feels_like']

    return f"feels like {feels_like}, condition: {condition}"


# "Отличная погодка для х"
# "На улице сильный дождик, но мы все равно можем попробовать найти наилучший маршрут!"