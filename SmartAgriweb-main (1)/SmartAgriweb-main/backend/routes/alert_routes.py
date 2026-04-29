from flask import Blueprint, request, jsonify
from models.alerts_model import AlertModel
from utils.response_format import success, error

alert_bp = Blueprint("alerts", __name__)


@alert_bp.route("/")
def get_alerts():
    rows = AlertModel.get_active()
    return jsonify(AlertModel.format_for_frontend(rows))


@alert_bp.route("/all")
def get_all_alerts():
    rows = AlertModel.get_all()
    return jsonify(AlertModel.format_for_frontend(rows))


@alert_bp.route("/count")
def alert_count():
    return jsonify({"count": AlertModel.count_active()})


@alert_bp.route("/resolve/<int:alert_id>", methods=["POST"])
def resolve_alert(alert_id):
    AlertModel.resolve(alert_id)
    return jsonify(success("Alert resolved"))


@alert_bp.route("/create", methods=["POST"])
def create_alert():
    body = request.get_json(silent=True) or {}
    for field in ["type", "title", "message"]:
        if field not in body:
            return jsonify(error(f"Missing: {field}")), 400
    aid = AlertModel.create(body["type"], body["title"], body["message"])
    return jsonify(success("Alert created", {"id": aid})), 201
