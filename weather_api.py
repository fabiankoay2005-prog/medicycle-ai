import requests

API_KEY = "YOUR_OPENWEATHER_API_KEY"

def get_weather(city="Penang"):

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    res = requests.get(url).json()

    if "main" not in res:
        return {"temp": 30, "condition": "unknown"}

    return {
        "temp": res["main"]["temp"],
        "condition": res["weather"][0]["main"]
    }


def weather_factor(condition):

    if condition in ["Rain", "Thunderstorm"]:
        return 1.3
    elif condition == "Clouds":
        return 1.1
    elif condition == "Clear":
        return 1.0
    else:
        return 1.05