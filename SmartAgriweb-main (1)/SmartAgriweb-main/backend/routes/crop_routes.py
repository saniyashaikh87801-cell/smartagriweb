from flask import Blueprint, request, jsonify
from models.crops_model import CropModel
from services.crop_recommender import CropRecommender
from utils.response_format import error

import requests

crop_bp = Blueprint("crops", __name__)


@crop_bp.route("/search")
def crop_search():
    q = request.args.get("q", "").strip()
    if not q:
        return jsonify([])
    return jsonify(CropModel.search(q))


@crop_bp.route("/<crop_key>")
def crop_detail(crop_key):
    crop = CropModel.get(crop_key)
    if not crop:
        return jsonify(error(f"Crop '{crop_key}' not found")), 404

url = "https://api.thingspeak.com/channels/YOUR_CHANNEL_ID/feeds.json?api_key=YOUR_READ_API_KEY&results=10"

response = requests.get(url)
data = response.json()
field1_values = [feed.get('field1') for feed in data.get('feeds', [])]
field2_values = [feed.get('field2') for feed in data.get('feeds', [])]
field3_values = [feed.get('field3') for feed in data.get('feeds', [])]
field4_values = [feed.get('field4') for feed in data.get('feeds', [])]
field5_values = [feed.get('field5') for feed in data.get('feeds', [])]




print("Temp:",field1_values)
print("Humd:",field2_values)
print("Soil_Moist:",field3_values)
print("Soil_type:",field4_values)
print("Season:",field5_values)


@crop_bp.route("/recommend", methods=["POST"])
def recommend():
    """
    Body: { temperature, humidity, soil_moisture, soil_type, season }
    Returns: list of recommended crops with scores.
    """
    body = request.get_json(silent=True) or {}
    recommendations = CropRecommender.recommend(
        temperature=float(body.get("temperature", 28)),
        humidity=int(body.get("humidity", 60)),
        soil_moisture=int(body.get("soil_moisture", 45)),
        soil_type=body.get("soil_type", "loamy"),
        season=body.get("season", "Summer"),
    )
    return jsonify(recommendations)
