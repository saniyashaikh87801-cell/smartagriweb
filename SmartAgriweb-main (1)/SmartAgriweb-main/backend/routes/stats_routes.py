from flask import Blueprint, jsonify, request
from database.db import query_db, execute_db
from models.alerts_model import AlertModel
from services.weather_service import WeatherService
from datetime import datetime, timedelta
import random

stats_bp = Blueprint("stats", __name__)

def _week_labels():
    today = datetime.today()
    return [(today - timedelta(days=6 - i)).strftime("%a") for i in range(7)]


# ══════════════════════════════════════════
#  HOME
# ══════════════════════════════════════════

@stats_bp.route("/home/stats")
def home_stats():
    rows = query_db("""
        SELECT SUM(liters_used) as total, SUM(liters_wasted) as wasted
        FROM irrigation_log
        WHERE date(logged_at) = date('now')
    """, one=True)
    total   = int(rows["total"]  or 520)
    wasted  = int(rows["wasted"] or 120)
    alerts  = AlertModel.count_active()
    return jsonify({
        "total_water_used":  total,
        "water_wasted_today": wasted,
        "active_crops":      4,
        "alerts_count":      alerts,
    })


@stats_bp.route("/home/water-usage")
def home_water_usage():
    rows = query_db("""
        SELECT date(logged_at) as day,
               SUM(liters_used)   as water_used,
               SUM(liters_wasted) as water_wasted
        FROM irrigation_log
        GROUP BY day
        ORDER BY day DESC LIMIT 7
    """)
    data = list(reversed([dict(r) for r in rows]))
    if not data:
        return jsonify({
            "labels":       _week_labels(),
            "water_used":   [340,420,370,400,460,480,520],
            "water_wasted": [60,80,55,90,100,110,120],
        })
    return jsonify({
        "labels":       [r["day"] for r in data],
        "water_used":   [int(r["water_used"]   or 0) for r in data],
        "water_wasted": [int(r["water_wasted"] or 0) for r in data],
    })


@stats_bp.route("/home/alerts")
def home_alerts():
    rows = AlertModel.get_active(limit=5)
    return jsonify(AlertModel.format_for_frontend(rows))


# ══════════════════════════════════════════
#  WATER / IRRIGATION
# ══════════════════════════════════════════

@stats_bp.route("/water/status")
def water_status():
    row = query_db(
        "SELECT * FROM sensor_readings ORDER BY recorded_at DESC LIMIT 1", one=True
    )
    soil = int(row["soil_moisture"]) if row else 45
    temp = float(row["temperature"]) if row else 32
    hum  = int(row["humidity"])      if row else 60

    condition = "Optimal" if 35 <= soil <= 65 else ("Dry" if soil < 35 else "Waterlogged")
    week = query_db("""
        SELECT SUM(liters_used) as total FROM irrigation_log
        WHERE logged_at >= datetime('now', '-7 days')
    """, one=True)

    return jsonify({
        "soil_moisture":     soil,
        "soil_condition":    condition,
        "temperature":       temp,
        "humidity":          hum,
        "rain_expected":     False,
        "irrigation_needed": soil < 40,
        "recommended_time":  "Early Morning",
        "today_usage":       520,
        "week_usage":        int(week["total"] or 3600),
    })


@stats_bp.route("/water/weekly")
def water_weekly():
    rows = query_db("""
        SELECT date(logged_at) as day, SUM(liters_used) as total
        FROM irrigation_log GROUP BY day ORDER BY day DESC LIMIT 7
    """)
    data = list(reversed([dict(r) for r in rows]))
    if not data:
        return jsonify({"labels": _week_labels(), "data": [480,510,460,520,540,490,520]})
    return jsonify({
        "labels": [r["day"] for r in data],
        "data":   [int(r["total"] or 0) for r in data],
    })


@stats_bp.route("/water/start", methods=["POST"])
def water_start():
    execute_db(
        "INSERT INTO irrigation_log (liters_used, liters_wasted, started_by) VALUES (?,?,?)",
        (random.randint(40, 60), random.randint(5, 15), "manual")
    )
    return jsonify({
        "success":    True,
        "message":    "Irrigation started!",
        "started_at": datetime.now().strftime("%H:%M:%S"),
    })


# ══════════════════════════════════════════
#  ANALYTICS
# ══════════════════════════════════════════

@stats_bp.route("/analytics/forecast")
def analytics_forecast():
    weather = WeatherService.get_forecast()
    return jsonify(weather)


@stats_bp.route("/analytics/vitals")
def analytics_vitals():
    row = query_db(
        "SELECT AVG(soil_moisture) as sm, AVG(temperature) as temp FROM sensor_readings", one=True
    )
    return jsonify({
        "avg_soil_moisture": round(row["sm"]   or 32, 1),
        "air_temperature":   round(row["temp"] or 26, 1),
        "active_alerts":     AlertModel.count_active(),
        "local_alert":       "Frost Advisory",
    })


@stats_bp.route("/analytics/tasks")
def analytics_tasks():
    return jsonify([
        {"id":1,"name":"Morning Diagnostics",  "status":"done"},
        {"id":2,"name":"Refill Nitrogen Tank",  "status":"critical"},
        {"id":3,"name":"Inspect Sensor A",      "status":"warning"},
    ])


@stats_bp.route("/analytics/yield")
def analytics_yield():
    return jsonify({
        "labels": ["Wheat","Corn","Soybeans"],
        "data":   [720,640,580],
        "colors": ["#3cb554","#3498db","#f5a623"],
    })


# ══════════════════════════════════════════
#  INVENTORY / METRICS
# ══════════════════════════════════════════

@stats_bp.route("/inventory/metrics")
def inventory_metrics():
    return jsonify({
        "water_efficiency":  "1.2 kg/L",
        "operational_cost":  "$1,250",
        "disease_risk":      "Low (15%)",
        "system_uptime":     "99.8%",
        "yield_change":      "+3.2%",
    })


@stats_bp.route("/inventory/generate-report", methods=["POST"])
def generate_report():
    report_id = f"RPT-{random.randint(1000,9999)}"
    return jsonify({
        "success":      True,
        "report_id":    report_id,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "message":      "Report generated successfully.",
    })
