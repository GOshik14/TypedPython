from enum import Enum

from typing import NamedTuple
from datetime import datetime

from coordinates import Coordinates

import urllib.request
from urllib.error import URLError

import json
from json import JSONDecodeError

from config import OPENWEATHER_URL_TEMPLATE
from exceptions import ApiServiceError

import ssl


Celsius = int  # Alias for int


class WeatherType(Enum):
    THUNDERSTORM = "Гроза"
    DRIZZLE = "Изморозь"
    RAIN = "Дождь"
    SNOW = "Снег"
    CLEAR = "Ясно"
    FOG = "Туман"
    CLOUDS = "Облачно"


class Weather(NamedTuple):
    temperature: Celsius
    weather_type: WeatherType
    sunrise: datetime
    sunset: datetime
    city: str


def get_weather(coordinates: Coordinates) -> Weather:
    """Requests weather in OPENWEATHER API and return it"""
    openweather_response = _get_openweather_response(
        longitude=coordinates.longitude, latitude=coordinates.latitude)
    weather = _parse_openweather_response(openweather_response)
    return weather


def _get_openweather_response(longitude: float, latitude: float) -> str:
    ssl._create_default_https_context = ssl._create_unverified_context

    url = OPENWEATHER_URL_TEMPLATE.format(longitude=longitude,
                                          latitude=latitude)
    try:
        return urllib.request.urlopen(url).read()
    except URLError:
        raise ApiServiceError


def _parse_openweather_response(openweather_response: str) -> Weather:
    try:
        response_dct = json.loads(openweather_response)
    except JSONDecodeError:
        raise ApiServiceError

    try:
        weather = Weather(
                temperature=response_dct["main"]["temp"],
                weather_type=_parse_weather_type(
                    response_dct["weather"][0]["id"]),
                sunrise=datetime.fromtimestamp(response_dct["sys"]["sunrise"]),
                sunset=datetime.fromtimestamp(response_dct["sys"]["sunset"]),
                city=response_dct["name"]
                )
    except (KeyError, IndexError, TypeError):
        raise ApiServiceError

    return weather


def _parse_weather_type(weather_id: int) -> WeatherType:
    weather_types = {
        "2": WeatherType.THUNDERSTORM,
        "3": WeatherType.DRIZZLE,
        "5": WeatherType.RAIN,
        "6": WeatherType.SNOW,
        "7": WeatherType.FOG,
        "800": WeatherType.CLEAR,
        "80": WeatherType.CLOUDS
    }
    for _id, _weather_type in weather_types.items():
        if str(weather_id).startswith(_id):
            return _weather_type
    raise ApiServiceError


if __name__ == '__main__':
    print(get_weather(Coordinates(latitude=52.7, longitude=6.2)))
