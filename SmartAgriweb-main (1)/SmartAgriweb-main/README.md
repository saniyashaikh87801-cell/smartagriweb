# 🌱 SmartAgriWeb

A full-stack IoT-powered Smart Agriculture Dashboard for real-time farm monitoring, irrigation control, and crop management.

---

## 🏗️ Project Structure

```
SmartAgriWeb/
├── backend/          # Python Flask API
├── frontend/         # HTML/JS Dashboard (single-file, no build needed)
├── iot/              # ESP32 Arduino firmware
└── docs/             # Documentation
```

---

## 🚀 Quick Start

### 1. Backend Setup

```bash
cd backend
pip install -r requirements.txt
python app.py
```

Open: http://localhost:5500

### 2. Environment Variables (optional)

Create a `.env` file in `backend/`:
```
OPENWEATHER_API_KEY=your_key_here
CITY=Mumbai
PORT=5500
DEBUG=true
```

### 3. ESP32 Setup

1. Open `iot/esp32/esp32_smart_agri.ino` in Arduino IDE
2. Edit `configs.h` — add your WiFi + server IP
3. Install libraries: DHT, BH1750, ArduinoJson
4. Flash to your ESP32

---

## 🔌 API Endpoints

See `docs/API_Endpoints.md` for full reference.

Key endpoints:
- `GET /api/sensors/live` — latest sensor reading
- `POST /api/sensors/ingest` — ESP32 posts data here
- `GET /api/crops/search?q=tomato` — search crops
- `GET /api/analytics/forecast` — weather forecast
- `POST /api/water/start` — trigger irrigation

---

## 📡 Hardware Required

See `docs/Hardware_List.md` for full list.

- ESP32 DevKit
- DHT22 (Temperature + Humidity)
- Capacitive Soil Moisture Sensor
- BH1750 Light Sensor
- 5V Relay Module (for pump)

---

## 🔑 Features

- 📊 Live dashboard with real-time charts
- 🌡️ Sensor monitoring (temperature, humidity, soil moisture)
- 💧 Smart irrigation control
- 🌿 18+ crop database with water requirements
- 🤖 Crop recommendation engine
- ⚠️ Rule-based alert system
- 🌤️ Live weather forecast (OpenWeatherMap)
- 📱 Responsive UI
