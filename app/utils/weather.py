import requests

from cachetools import func

url = 'https://wttr.in/stpetersburg?format=j1'

windy_cond = 'На улице сейчас сильный ветерок, дважды подумайте о том, что вы наденете!' #ветренно
cold_cond = 'В Петербурге сейчас холодновато, одевайтесь потеплее!' #холодно
hot_cond = 'В культурной столице сейчас очень жарко, не забудьте взять плавки!' #жарко
rain_cond = 'В городе сейчас идет дождик, учтите это при выборе маршрута!' #дождь
perfect_cond = 'На улице сейчас идеальная погода для любого вида прогулки!' #идеально


@func.ttl_cache(maxsize=1, ttl=14400)
def get_weather():
    r = requests.get(url)
    json_fact = r.json()['current_condition']
    feels_like = int(json_fact[0]['FeelsLikeC'])
    wind_speed = float(json_fact[0]['windspeedKmph'])

    if feels_like < 8:
        return cold_cond
    elif feels_like >= 23:
        return hot_cond
    elif wind_speed > 4.5:
        return windy_cond
    else:
        return perfect_cond
