from dotenv import load_dotenv
import requests
import sys
import os


load_dotenv()
API_KEY = os.getenv('API_KEY')


def set_user_city() -> str:
    config = open("config.txt", "w")
    user_city = input("Enter a city name: ").lower().title()
    config.write(user_city)
    config.close()

    return user_city


def geocode_user_city(user_city: str) -> tuple[str, float, float]:
    request_url = f"http://api.openweathermap.org/geo/1.0/direct?q={user_city}&limit=1&appid={API_KEY}"
    request_data = requests.get(request_url).json()

    if len(request_data) > 0:
        user_city_lat = request_data[0]['lat']
        user_city_lon = request_data[0]['lon']

        return user_city, user_city_lat, user_city_lon

    else:
        print("An unexpected error occurred, please try with other city.")

        return geocode_user_city(set_user_city())


def get_user_city_weather(user_city: str, lat: float, lon: float) -> None:
    request_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}"
    request_data = requests.get(request_url).json()

    user_city_temp = request_data['main']['temp']
    user_city_weather = request_data['weather'][0]['main']
    user_city_wind = request_data['wind']['speed']

    print_user_city_weather(user_city, convert_temp(user_city_temp), user_city_weather, convert_wind(user_city_wind))


def convert_temp(temp: float) -> int:
    return int(temp - 273.15)


def convert_wind(wind: float) -> int:
    return int(wind * 3.6)


def print_user_city_weather(user_city: str, user_city_temp: int, user_city_weather: str, user_city_wind: int):
    print(f"Current weather in {user_city}: {user_city_temp}C - {user_city_weather} (Wind: {user_city_wind}km/h)")


def get_user_input() -> str:
    while True:
        user_input = input("E - Exit, C - Change City: ")

        if user_input in ("E", "e"):
            return "e"

        if user_input in ("C", "c"):
            return "c"


def main():
    config = open("config.txt", "r")
    user_city = config.read()
    config.close()

    if len(user_city) < 1:
        user_city = set_user_city()

    while True:
        user_city, user_city_lat, user_city_lon = geocode_user_city(user_city)
        get_user_city_weather(user_city, user_city_lat, user_city_lon)

        user_input = get_user_input()

        if user_input in ("E", "e"):
            print("Exiting Program...")
            sys.exit()

        if user_input in ("C", "c"):
            user_city = set_user_city()


if __name__ == '__main__':
    main()
    