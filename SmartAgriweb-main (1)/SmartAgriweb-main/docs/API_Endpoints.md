# SmartAgriWeb — API Endpoints

Base URL: `http://localhost:5500`

---

## 🌡️ Sensors

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/sensors/live` | Latest sensor reading (simulated or DB) |
| GET | `/api/sensors/charts` | Weekly temperature + soil moisture chart data |
| POST | `/api/sensors/ingest` | ESP32 posts real sensor data |

**POST /api/sensors/ingest**
```json
{
  "temperature": 31.5,
  "humidity": 62,
  "soil_moisture": 45,
  "light_lux": 620
}
```

---

## ⚠️ Alerts

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/alerts/` | Get active alerts |
| GET | `/api/alerts/all` | Get all alerts (including resolved) |
| GET | `/api/alerts/count` | Count of active alerts |
| POST | `/api/alerts/resolve/<id>` | Resolve an alert |
| POST | `/api/alerts/create` | Create a new alert |

---

## 🌿 Crops

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/crops/search?q=tomato` | Search crops by name or category |
| GET | `/api/crops/<key>` | Get full crop details |
| POST | `/api/crops/recommend` | Get crop recommendations |

**POST /api/crops/recommend**
```json
{
  "temperature": 28,
  "humidity": 65,
  "soil_moisture": 45,
  "soil_type": "loamy",
  "season": "Summer"
}
```

---

## 🏠 Home / Dashboard

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/home/stats` | Summary stats (water, crops, alerts) |
| GET | `/api/home/water-usage` | Weekly water usage chart |
| GET | `/api/home/alerts` | Top active alerts for dashboard |

---

## 💧 Water / Irrigation

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/water/status` | Current soil + irrigation status |
| GET | `/api/water/weekly` | Weekly irrigation chart |
| POST | `/api/water/start` | Trigger irrigation session |

---

## 📊 Analytics

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/analytics/forecast` | 7-day weather forecast |
| GET | `/api/analytics/vitals` | Farm vitals summary |
| GET | `/api/analytics/tasks` | Farm task list |
| GET | `/api/analytics/yield` | Yield chart data |

---

## 📦 Inventory

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/inventory/metrics` | Performance metrics |
| POST | `/api/inventory/generate-report` | Generate report |
