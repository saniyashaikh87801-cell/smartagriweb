# SmartAgriWeb — Hardware List

## 🧠 Microcontroller

| Component | Model | Purpose | Approx. Cost |
|-----------|-------|---------|-------------|
| Microcontroller | ESP32 DevKit V1 | Main IoT controller, WiFi | ₹350 / $4 |

---

## 🌡️ Sensors

| Component | Model | Pin | Purpose | Cost |
|-----------|-------|-----|---------|------|
| Temp + Humidity | DHT22 | GPIO 4 | Air temperature & humidity | ₹180 / $2 |
| Soil Moisture | Capacitive v1.2 | GPIO 34 (ADC) | Soil water content | ₹150 / $2 |
| Light Sensor | BH1750 FVI | I2C (SDA/SCL) | Light intensity (lux) | ₹120 / $1.5 |

> ⚠️ Use **capacitive** soil moisture sensor (not resistive) — resistive sensors corrode.

---

## 💧 Irrigation

| Component | Model | Purpose | Cost |
|-----------|-------|---------|------|
| Relay Module | 5V Single Channel | Control irrigation pump | ₹80 / $1 |
| Water Pump | 12V Submersible Mini | Pump water to field | ₹250 / $3 |
| Tubing | 8mm silicone | Water delivery | ₹100 / $1.5 |

---

## ⚡ Power

| Component | Spec | Purpose | Cost |
|-----------|------|---------|------|
| Power Supply | 5V 2A USB-C | Power ESP32 | ₹200 / $2.5 |
| 12V Adapter | 1A | Power pump relay | ₹150 / $2 |

---

## 🔌 Wiring Summary

```
ESP32 GPIO 4  ──── DHT22 DATA
ESP32 GPIO 34 ──── Soil Sensor AOUT
ESP32 GPIO 21 ──── BH1750 SDA
ESP32 GPIO 22 ──── BH1750 SCL
ESP32 GPIO 26 ──── Relay IN
3.3V          ──── Sensors VCC
GND           ──── All GND
```

---

## 📦 Total Estimated Cost

| Category | Cost (INR) | Cost (USD) |
|----------|-----------|-----------|
| Microcontroller | ₹350 | $4 |
| Sensors | ₹450 | $5.5 |
| Irrigation | ₹430 | $5.5 |
| Power | ₹350 | $4.5 |
| **Total** | **~₹1,580** | **~$20** |

---

## 🛒 Where to Buy (India)

- [Robu.in](https://robu.in)
- [Robocraze](https://robocraze.com)
- [Amazon India](https://amazon.in)
- Local electronics market (Lamington Road, SP Road)
