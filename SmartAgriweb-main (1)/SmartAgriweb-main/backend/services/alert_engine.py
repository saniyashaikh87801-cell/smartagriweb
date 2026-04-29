from models.alerts_model import AlertModel
import os

class AlertEngine:
    """
    Rule-based alert engine.
    Call AlertEngine.evaluate(sensor_data) after each sensor reading.
    """

    TEMP_MAX       = float(os.environ.get("TEMP_MAX",  40))
    TEMP_MIN       = float(os.environ.get("TEMP_MIN",  10))
    HUM_MIN        = int(os.environ.get("HUMIDITY_MIN", 30))
    SOIL_MIN       = int(os.environ.get("SOIL_MIN",    20))
    SOIL_MAX       = int(os.environ.get("SOIL_MAX",    80))

    @staticmethod
    def evaluate(sensor: dict):
        """
        Check sensor data against thresholds.
        Creates alerts in DB for any violations.
        Returns list of new alerts created.
        """
        alerts_created = []
        temp  = sensor.get("temperature", 25)
        hum   = sensor.get("humidity", 50)
        soil  = sensor.get("soil_moisture", 45)

        if temp > AlertEngine.TEMP_MAX:
            aid = AlertModel.create(
                "danger",
                "High Temperature Alert",
                f"Temperature {temp}°C exceeds max threshold of {AlertEngine.TEMP_MAX}°C"
            )
            alerts_created.append(aid)

        if temp < AlertEngine.TEMP_MIN:
            aid = AlertModel.create(
                "warning",
                "Low Temperature Alert",
                f"Temperature {temp}°C is below safe minimum of {AlertEngine.TEMP_MIN}°C"
            )
            alerts_created.append(aid)

        if hum < AlertEngine.HUM_MIN:
            aid = AlertModel.create(
                "warning",
                "Low Humidity Alert",
                f"Humidity {hum}% is below recommended {AlertEngine.HUM_MIN}%"
            )
            alerts_created.append(aid)

        if soil < AlertEngine.SOIL_MIN:
            aid = AlertModel.create(
                "danger",
                "Critical Soil Moisture",
                f"Soil moisture {soil}% — irrigation required immediately"
            )
            alerts_created.append(aid)

        if soil > AlertEngine.SOIL_MAX:
            aid = AlertModel.create(
                "warning",
                "Over-Irrigation Detected",
                f"Soil moisture {soil}% is too high — stop irrigation"
            )
            alerts_created.append(aid)

        return alerts_created
