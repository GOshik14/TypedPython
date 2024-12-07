from datetime import datetime
from pathlib import Path
from typing import TypedDict
import json

from weather_api_service import Weather, WeatherType
from weather_formatter import format_weather


class HistoryRecord(TypedDict):
    date: str
    weather: str


class WeatherStorage:
    """Interface for any storage saving weather"""
    def save(self, weather: Weather) -> None:
        raise NotImplementedError


class PlainWeatherStorage(WeatherStorage):
    """Store weather in plain text file"""
    def __init__(self, file: Path):
        self._file = file

    def save(self, weather: Weather) -> None:
        now = datetime.now()
        formated_weather = format_weather(weather)
        with open(self._file, "a") as f:
            f.write(f"{now}\n{formated_weather}\n")


class JSONFileWeatherStorage(WeatherStorage):
    """Store weather in json file"""
    def __init__(self, jsonfile: Path) -> None:
        self._jsonfile = jsonfile
        self._init_storage()

    def save(self, weather: Weather) -> None:
        history = self._read_history()
        history.append({
            "date": str(datetime.now()),
            "weather": format_weather(weather)
        })
        self._write(history)

    def _init_storage(self) -> None:
        if not self._jsonfile.exists():
            self._jsonfile.write_text("[]")

    def _read_history(self) -> list[HistoryRecord]:
        with open(self._jsonfile, "r") as f:
            return json.load(f)

    def _write(self, history: list[HistoryRecord]) -> None:
        with open(self._jsonfile, "w") as f:
            json.dump(history, f, ensure_ascii=False, indent=4)


def save_history(weather: Weather, weather_storage: WeatherStorage) -> None:
    weather_storage.save(weather)


if __name__ == "__main__":
    plain_weather_storage = PlainWeatherStorage(
        Path("./storage/storage_sample.txt"))
    plain_weather_storage.save(Weather(
        temperature=25,
        weather_type=WeatherType.CLEAR,
        sunrise=datetime.fromisoformat("2022-05-03 04:00:00"),
        sunset=datetime.fromisoformat("2022-05-03 20:00:00"),
        city="Moscow"
    ))
