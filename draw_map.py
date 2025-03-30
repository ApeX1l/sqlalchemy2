import requests
from io import BytesIO


def draw_map(address_ll):
    apikey = "604d9abb-48ac-4c58-9c7f-c0dca0c09445"
    map_params = {
        "ll": address_ll,
        'z': 10,
        "apikey": apikey
    }
    map_api_server = "https://static-maps.yandex.ru/v1?"
    response = requests.get(map_api_server, params=map_params)
    with open('static/img/map.png', "wb") as file:
        file.write(response.content)
