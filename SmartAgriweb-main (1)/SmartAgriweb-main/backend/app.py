from flask import Flask, send_from_directory, session, redirect
from flask_cors import CORS
import os

from config import Config
from database.db import init_db
from routes.sensor_routes import sensor_bp
from routes.alert_routes import alert_bp
from routes.crop_routes import crop_bp
from routes.stats_routes import stats_bp
from routes.auth_routes import auth_bp

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(os.path.dirname(BASE_DIR), "frontend", "public")

app = Flask(__name__, static_folder=FRONTEND_DIR)
app.config.from_object(Config)
CORS(app)

# ── Register Blueprints ──
app.register_blueprint(sensor_bp, url_prefix="/api/sensors")
app.register_blueprint(alert_bp,  url_prefix="/api/alerts")
app.register_blueprint(crop_bp,   url_prefix="/api/crops")
app.register_blueprint(stats_bp,  url_prefix="/api")
app.register_blueprint(auth_bp)          # login / signup / logout (no prefix)

# ── Serve Frontend (protected) ──
@app.route("/")
def index():
    if "user_email" not in session:
        return redirect("/login")
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.route("/<path:path>")
def static_files(path):
    # Static assets pass through freely
    if path.startswith("icons/") or path.endswith((".js", ".css", ".png", ".ico", ".svg")):
        return send_from_directory(FRONTEND_DIR, path)
    if "user_email" not in session:
        return redirect("/login")
    return send_from_directory(FRONTEND_DIR, path)

@app.route("/chatbot")
def chatbot():
    if "user_email" not in session:
        return redirect("/login")
    SANIYA_DIR = os.path.join(os.path.dirname(BASE_DIR), "saniya")
    return send_from_directory(SANIYA_DIR, "index.html")

@app.route("/saniya/<path:path>")
def saniya_files(path):
    SANIYA_DIR = os.path.join(os.path.dirname(BASE_DIR), "saniya")
    return send_from_directory(SANIYA_DIR, path)

# ── Init DB on startup ──
with app.app_context():
    init_db()

if __name__ == "__main__":
    app.run(port=8000, debug=True)