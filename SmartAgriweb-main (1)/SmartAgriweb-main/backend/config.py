import os

class Config:
    # IMPORTANT: change this to a strong random value in production
    SECRET_KEY         = os.environ.get("SECRET_KEY", "smartagri-secret-key-change-in-prod-2024!")
    DEBUG              = os.environ.get("DEBUG", "true").lower() == "true"
    PORT               = int(os.environ.get("PORT", 5500))

    # Database
    DATABASE_PATH      = os.path.join(os.path.dirname(__file__), "database", "smartagri.db")

    # Session cookies
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    # OpenWeatherMap API (replace with your key)
    OPENWEATHER_API_KEY = os.environ.get("OPENWEATHER_API_KEY", "YOUR_API_KEY_HERE")
    OPENWEATHER_CITY    = os.environ.get("CITY", "Mumbai")
    OPENWEATHER_UNITS   = "metric"

    # ThingSpeak (public channel feeds JSON — override channel via env if needed)
    THINGSPEAK_FEEDS_URL = os.environ.get(
        "THINGSPEAK_FEEDS_URL",
        "https://api.thingspeak.com/channels/3303227/feeds.json?results=1",
    )

    # Sensor thresholds for alert engine
    TEMP_MAX            = 40.0
    TEMP_MIN            = 10.0
    HUMIDITY_MIN        = 30
    SOIL_MOISTURE_MIN   = 20
    SOIL_MOISTURE_MAX   = 80