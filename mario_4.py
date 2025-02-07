from io import BytesIO
import requests
from PIL import Image


def par(x, y):
    coordx = str(float(x[0]) - float(y[0]))
    coordy = str(float(x[1]) - float(y[1]))
    return [coordx, coordy]


def get_map_params(toponym_coordinates, toponym_upcorner, toponym_lowercorner):
    delta = par(toponym_upcorner, toponym_lowercorner)
    longitude, latitude = toponym_coordinates.split(" ")
    ll = ",".join([longitude, latitude])
    spn = ",".join(delta)
    return ll, spn


def get_nearest_pharmacy(ll):
    search_api_server = "https://search-maps.yandex.ru/v1/"
    search_params = {
        "apikey": "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3",
        "text": "аптека",
        "lang": "ru_RU",
        "ll": ll,
        "type": "biz",
    }

    response = requests.get(search_api_server, params=search_params)
    response.raise_for_status()

    json_response = response.json()
    organizations = json_response["features"]
    if len(organizations) > 0:
        organization = organizations[0]
        org_name = organization["properties"]["name"]
        org_address = organization["properties"]["description"]
        org_hours = organization["properties"]["CompanyMetaData"]["Hours"]["text"]
        # org_distance = organization["properties"]["boundedBy"][0]["distance"] # removed this line
        return {
            "name": org_name,
            "address": org_address,
            "hours": org_hours,
            "coordinates": organization["geometry"]["coordinates"],
            # "distance": org_distance # removed this line
        }
    else:
        return None


toponym_to_find = 'Москва, Льва Толстого, 7 '

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"
}

response = requests.get(geocoder_api_server, params=geocoder_params)
response.raise_for_status()

json_response = response.json()
toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
toponym_coordinates = toponym["Point"]["pos"]
toponym_upcorner = toponym['boundedBy']['Envelope']['upperCorner'].split()
toponym_lowercorner = toponym['boundedBy']['Envelope']['lowerCorner'].split()

ll, spn = get_map_params(toponym_coordinates, toponym_upcorner, toponym_lowercorner)

map_params = {
    "ll": ll,
    "spn": spn,
    "l": "map",
    "pt": f"{ll},pm2dgl"
}

nearest_pharmacy = get_nearest_pharmacy(ll)
if nearest_pharmacy:
    pharmacy_name = nearest_pharmacy["name"]
    pharmacy_address = nearest_pharmacy["address"]
    pharmacy_hours = nearest_pharmacy["hours"]
    # pharmacy_distance = nearest_pharmacy["distance"] # removed this line
    pharmacy_coordinates = nearest_pharmacy["coordinates"]
    map_params["pt"] += f"~{pharmacy_coordinates[0]},{pharmacy_coordinates[1]},pm2dgl"

    print(f"Ближайшая аптека: {pharmacy_name}")
    print(f"Адрес: {pharmacy_address}")
    print(f"Время работы: {pharmacy_hours}")
    # print(f"Расстояние от исходного адреса: {pharmacy_distance} м") # removed this line
else:
    print("Аптеки не найдены")
map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)
response.raise_for_status()

Image.open(BytesIO(response.content)).show()