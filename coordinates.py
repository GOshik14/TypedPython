from typing import NamedTuple
from typing import Literal

import json
from json import JSONDecodeError

import urllib.request
from urllib.error import URLError

from exceptions import CantGetCoordinates

from config import USE_ROUNDED_COORDINATES

url = "https://ipinfo.io/json"


class Coordinates(NamedTuple):
    latitude: float
    longitude: float


def get_coordinates() -> Coordinates:
    """Return current coordinates"""
    response = _get_response(url)
    json_dict = _parse_json_responsed(response)
    coordinates: Coordinates = _parse_json_to_coordinates(json_dict)
    if USE_ROUNDED_COORDINATES:
        coordinates = _round_coordinates(coordinates)
    return coordinates


def _get_response(url: str) -> str:
    try:
        return urllib.request.urlopen(url).read()
    except URLError:
        raise CantGetCoordinates


def _parse_json_responsed(responced_json: str) -> dict[Literal["loc"], str]:
    try:
        return json.loads(responced_json)
    except JSONDecodeError:
        raise CantGetCoordinates


def _parse_json_to_coordinates(json_dct:
                               dict[Literal["loc"], str]) -> Coordinates:
    try:
        return Coordinates(*map(float, json_dct["loc"].split(',')))
    except (ValueError, KeyError):
        raise CantGetCoordinates


def _round_coordinates(coordinates: Coordinates) -> Coordinates:
    try:
        return Coordinates(*map(lambda c: round(c, 1), coordinates))
    except (ValueError, TypeError):
        raise CantGetCoordinates


if __name__ == "__main__":
    print(get_coordinates())
