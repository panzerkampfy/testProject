import datetime
import requests
import os
import json


def get_fact_today() -> str:
    date = datetime.datetime.now().strftime("%m/%d")
    path = 'http://numbersapi.com/' + date + '/date'
    response = requests.get(path)
    response = str(response.content)[2:-1]
    return response


def get_weather_today() -> float:
    city = str(1489425)
    apikey = str(os.environ.get('APPID_WEATHER'))
    path = 'http://api.openweathermap.org/data/2.5/weather?id=' + city + '&appid=' + apikey
    response = requests.get(path)
    response = json.loads(response.content.decode('utf-8'))
    temp = float(response.get('main').get('temp'))
    temp = temp - 273.15
    return temp
