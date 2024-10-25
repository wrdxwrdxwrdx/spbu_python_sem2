import argparse
from datetime import datetime

import matplotlib.pyplot as plt
import requests

from src.homeworks.homework_3.ORM import *


@dataclass
class WeatherSub(JsonORM):
    id: int
    main: str
    description: str


@dataclass
class Main(JsonORM):
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float


@dataclass
class ListSub(JsonORM):
    dt: int
    main: Main
    weather: list[WeatherSub]
    visibility: int


@dataclass
class Json(JsonORM):
    list: list[ListSub]


def get_json(link: str) -> dict:
    response = requests.get(link)
    json_dict = response.json()
    if json_dict.get("cod", None) == 401:
        raise ValueError("Invalid API KEY")
    if json_dict.get("cod", None) == "404":
        raise ValueError("Invalid city")
    return json_dict


def get_city_info(api_key: str, city: str) -> str:
    json_dict = get_json(f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric")

    forecast: Json = Json.with_json(json_dict)
    temp = forecast.list[0].main.temp
    min_temp = forecast.list[0].main.temp_min
    max_temp = forecast.list[0].main.temp_max
    date = datetime.fromtimestamp(forecast.list[0].dt).strftime("%A, %B %d, %Y %I:%M:%S")
    visibility = forecast.list[0].visibility
    extra_info = forecast.list[0].weather[0].description
    return (
        f"weather info about {city} ({date}):\n"
        f"  temperature: {temp}°C (from {min_temp}°C to {max_temp}°C in 3 last hours)\n"
        f"  visibility: {visibility}\n"
        f"  extra_info: {extra_info}"
    )


def create_temp_graph(api_key: str, city: str, output_path: str = "graph") -> None:
    time = []
    temp = []
    json_dict = get_json(f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric")
    if json_dict is None:
        raise ValueError("Incorrect city name")

    forecast: Json = Json.with_json(json_dict)
    for moment in forecast.list:
        temp.append(moment.main.temp)
        time.append(moment.dt)

    plt.title(f"temperature in {city}")
    plt.plot(time, temp)

    plt.xlabel("time")
    plt.ylabel("temperature")

    plt.savefig(output_path)


def main(command: str, city: str, api_key: str) -> None:
    if command == "info":
        print(get_city_info(api_key, city))
    elif command == "temp_graph":
        create_temp_graph(api_key, city)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--command", type=str, choices=["info", "temp_graph"], help="Enter command 'info' or 'temp_graph'"
    )
    parser.add_argument("--city", type=str, help="Enter the city you want to find out information about")
    parser.add_argument("--api_key", type=str, help="Enter openweathermap apikey")
    try:
        main(**vars(parser.parse_args()))
    except Exception as error:
        print(error)
