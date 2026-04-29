from flask import Blueprint, request, jsonify, current_app
import json
import requests
from models.sensor_model import SensorModel
from utils.response_format import success, error
from datetime import datetime, timedelta

sensor_bp = Blueprint("sensors", __name__)


def _parse_ts_field(value):
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


@sensor_bp.route("/thingspeak")
def sensors_thingspeak():
    """Latest channel fields from ThingSpeak (field1–4: temp, humidity, irrigation, CO₂)."""
    url = current_app.config.get("THINGSPEAK_FEEDS_URL")
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        payload = response.json()
    except requests.exceptions.RequestException as e:
        return jsonify(error(f"ThingSpeak request failed: {e}", 502)), 502
    except json.JSONDecodeError as e:
        return jsonify(error(f"Invalid JSON from ThingSpeak: {e}", 502)), 502

    feeds = payload.get("feeds") or []
    if not feeds:
        return jsonify(error("No feeds in ThingSpeak response", 404)), 404

    feed = feeds[0]
    out = {
        "temperature": _parse_ts_field(feed.get("field1")),
        "humidity": _parse_ts_field(feed.get("field2")),
        "irrigation": _parse_ts_field(feed.get("field3")),
        "co2": _parse_ts_field(feed.get("field4")),
        "created_at": feed.get("created_at"),
        "entry_id": feed.get("entry_id"),
    }
    return jsonify(success("ThingSpeak data", out))


@sensor_bp.route("/live")
def sensors_live():
    """Live sensor reading — saves simulated value to DB each call."""
    data = SensorModel.simulate_and_save()
    return jsonify(data)


@sensor_bp.route("/charts")
def sensors_charts():
    """Weekly chart data from DB."""
    rows = SensorModel.get_weekly()
    labels, temps, soils = [], [], []
    today = datetime.today()
    day_names = [(today - timedelta(days=6 - i)).strftime("%a") for i in range(7)]

    if rows:
        for r in rows:
            temps.append(r["temperature"])
            soils.append(r["soil_moisture"])
        labels = day_names[:len(rows)]
    else:
        labels = day_names
        temps  = [29, 31, 32, 30, 31, 32, 31]
        soils  = [58, 55, 48, 50, 45, 42, 43]

    return jsonify({"labels": labels, "temperature": temps, "soil_moisture": soils})


@sensor_bp.route("/ingest", methods=["POST"])
def ingest():
    """
    ESP32 posts sensor data here.
    Payload: { temperature, humidity, soil_moisture, light_lux }
    """
    body = request.get_json(silent=True) or {}
    required = ["temperature", "humidity", "soil_moisture"]
    for field in required:
        if field not in body:
            return jsonify(error(f"Missing field: {field}")), 400

    rid = SensorModel.save(
        temperature=float(body["temperature"]),
        humidity=int(body["humidity"]),
        soil_moisture=int(body["soil_moisture"]),
        light_lux=float(body.get("light_lux", 0)),
        source="esp32"
    )
    return jsonify(success("Sensor data saved", {"id": rid})), 201
