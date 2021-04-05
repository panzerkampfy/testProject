import datetime
import json
import os

import requests

from table.models import User, PermissionOnBoard, Task, Column


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


def task_obj_permission(id, pk) -> PermissionOnBoard:
    column_id = Task.objects.get(id=pk).column.id
    return column_obj_permission(id, column_id)


def column_obj_permission(id, pk) -> PermissionOnBoard:
    board_id = Column.objects.get(id=pk).board.id
    return board_obj_permission(id, board_id)


def board_obj_permission(id, pk) -> PermissionOnBoard:
    obj = PermissionOnBoard.objects.filter(user_id=id, board_id=pk, permission=1).first()
    return obj
