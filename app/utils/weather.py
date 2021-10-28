import requests

from app.utils.config import YW_TOKEN


headers = {'X-Yandex-API-Key': YW_TOKEN}
url = 'https://api.weather.yandex.ru/v2/informers/?lat=59.9311&lon=30.3609&lang=ru&limit=1'

windy_cond = 'На улице сейчас сильный ветерок, дважды подумайте о том, что вы наденете!' #ветренно
cold_cond = 'В Петербурге сейчас холодновато, одевайтесь потеплее!' #холодно
hot_cond = 'В культурной столице сейчас очень жарко, не забудьте взять плавки!' #жарко
rain_cond = 'В городе сейчас идет дождик, учтите это при выборе маршрута!' #дождь
perfect_cond = 'На улице сейчас идеальная погода для любого вида прогулки!' #идеально


def get_weather():
    r = requests.get(url, headers=headers)
    print(r.status_code)
    json_fact = r.json()['fact']
    condition = json_fact['condition']
    feels_like = json_fact['feels_like']
    wind_speed = json_fact['wind_speed']

    if 'rain' in condition:
        return rain_cond
    elif feels_like < 8:
        return cold_cond
    elif feels_like >= 23:
        return hot_cond
    elif wind_speed > 4.5:
        return windy_cond
    else:
        return perfect_cond
