import datetime
import requests
import os
import json
from table.models import User


def get_fact_today() -> str:
    date = datetime.datetime.now().strftime("%m/%d")
    path = 'http://numbersapi.com/' + date + '/date'
    response = requests.get(path)
    response = str(response.content)[2:-1]
    return response


def get_weather_today(user_id) -> float:
    city = User.objects.get(id=user_id).city
    if city is None or "":
        return None
    apikey = str(os.environ.get('APPID_WEATHER'))
    path = 'http://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid=' + apikey
    response = requests.get(path)
    response = json.loads(response.content.decode('utf-8'))
    temp = float(response.get('main').get('temp'))
    temp = temp - 273.15
    return temp
