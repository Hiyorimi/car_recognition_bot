import requests
from typing import Tuple

from logics.exif_parsing import get_exif, get_exif_geotagging
from settings import GEOCODING_API_KEY

URL_TEMPLATE = "https://geocode-maps.yandex.ru/1.x/?apikey={api_key}&geocode={long_lat}&format=json"


def get_decimal_from_dms(dms: Tuple[float, float, float], ref: str) -> float:

    degrees = dms[0]
    minutes = dms[1] / 60.0
    seconds = dms[2] / 3600.0

    if ref in ['S', 'W']:
        degrees = -degrees
        minutes = -minutes
        seconds = -seconds

    return round(degrees + minutes + seconds, 5)


def get_coordinates(geotags) -> Tuple[float, float]:
    lat = get_decimal_from_dms(geotags['GPSLatitude'], geotags['GPSLatitudeRef'])
    lon = get_decimal_from_dms(geotags['GPSLongitude'], geotags['GPSLongitudeRef'])

    return lat, lon


def get_geocoding_response(lat, long):
    """Gets geocoding response from passed lat and long."""
    payload = {}
    headers = {}
    url = URL_TEMPLATE.format(
        api_key=GEOCODING_API_KEY,
        long_lat=','.join(
            (str(long), str(lat)),
        ),
    )
    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()


def parse_address_from_geocoding_response(geocoded_data: dict) -> str:
    return geocoded_data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['text']


def get_address_of_image(exif_data) -> str:
    lat, long = get_coordinates(
        get_exif_geotagging(
            exif_data,
        ),
    )
    address_data = get_geocoding_response(lat, long)
    address = parse_address_from_geocoding_response(address_data)
    return address