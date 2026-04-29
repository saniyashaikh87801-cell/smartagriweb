from database.db import query_db, execute_db
from datetime import datetime
import random

class SensorModel:

    @staticmethod
    def get_latest():
        """Get the most recent sensor reading."""
        row = query_db(
            "SELECT * FROM sensor_readings ORDER BY recorded_at DESC LIMIT 1",
            one=True
        )
        if row:
            return dict(row)
        return SensorModel._simulated()

    @staticmethod
    def get_weekly():
        """Get last 7 daily average readings."""
        rows = query_db("""
            SELECT
                date(recorded_at) as day,
                ROUND(AVG(temperature),1) as temperature,
                ROUND(AVG(humidity))      as humidity,
                ROUND(AVG(soil_moisture)) as soil_moisture
            FROM sensor_readings
            GROUP BY date(recorded_at)
            ORDER BY day DESC
            LIMIT 7
        """)
        return [dict(r) for r in reversed(rows)]

    @staticmethod
    def save(temperature, humidity, soil_moisture, light_lux=0, source="simulated"):
        """Insert a new sensor reading."""
        return execute_db(
            "INSERT INTO sensor_readings (temperature, humidity, soil_moisture, light_lux, source) VALUES (?,?,?,?,?)",
            (temperature, humidity, soil_moisture, light_lux, source)
        )

    @staticmethod
    def _simulated():
        """Fallback simulated reading."""
        return {
            "temperature":   round(random.uniform(29.0, 33.0), 1),
            "humidity":      random.randint(52, 64),
            "soil_moisture": random.randint(38, 50),
            "light_lux":     round(random.uniform(400, 900), 1),
            "source":        "simulated",
            "recorded_at":   datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    @staticmethod
    def simulate_and_save():
        """Generate a simulated reading and persist it."""
        data = SensorModel._simulated()
        SensorModel.save(
            data["temperature"], data["humidity"],
            data["soil_moisture"], data["light_lux"], "simulated"
        )
        data["timestamp"] = datetime.now().strftime("%H:%M:%S")
        return data
