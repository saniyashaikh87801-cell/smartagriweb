import requests
import os
from datetime import datetime, timedelta

class WeatherService:

    BASE_URL = "https://api.openweathermap.org/data/2.5"

    @staticmethod
    def get_forecast():
        """
        Fetch 7-day forecast from OpenWeatherMap.
        Falls back to static data if API key not configured.
        """
        api_key = os.environ.get("OPENWEATHER_API_KEY", "")
        city    = os.environ.get("CITY", "Mumbai")

        if not api_key or api_key == "YOUR_API_KEY_HERE":
            return WeatherService._fallback_forecast()

        try:
            url = f"{WeatherService.BASE_URL}/forecast"
            params = {
                "q":     city,
                "appid": api_key,
                "units": "metric",
                "cnt":   7,
            }
            resp = requests.get(url, params=params, timeout=5)
            resp.raise_for_status()
            data = resp.json()

            labels, icons, temps = [], [], []
            today = datetime.today()
            for i, item in enumerate(data["list"][:7]):
                labels.append((today + timedelta(days=i)).strftime("%a"))
                temp = round(item["main"]["temp"])
                temps.append(temp)
                desc = item["weather"][0]["main"]
                icons.append(WeatherService._icon_for(desc))

            return {
                "labels":   labels,
                "icons":    icons,
                "temps":    temps,
                "wind":     f"{round(data['list'][0]['wind']['speed'])} km/h",
                "humidity": data["list"][0]["main"]["humidity"],
            }
        except Exception as e:
            print(f"[WeatherService] API error: {e}, using fallback.")
            return WeatherService._fallback_forecast()

    @staticmethod
    def _icon_for(description: str) -> str:
        mapping = {
            "Clear":        "🌤",
            "Clouds":       "⛅",
            "Rain":         "🌧",
            "Drizzle":      "🌦",
            "Thunderstorm": "⛈",
            "Snow":         "❄️",
            "Mist":         "🌫",
            "Fog":          "🌫",
        }
        return mapping.get(description, "🌤")

    @staticmethod
    def _fallback_forecast():
        today = datetime.today()
        labels = [(today + timedelta(days=i)).strftime("%a") for i in range(7)]
        return {
            "labels":   labels,
            "icons":    ["⛅","🌤","🌥","🌧","🌧","⛅","🌤"],
            "temps":    [24, 26, 20, 13, 13, 15, 18],
            "wind":     "15 km/h NW",
            "humidity": 45,
        }
