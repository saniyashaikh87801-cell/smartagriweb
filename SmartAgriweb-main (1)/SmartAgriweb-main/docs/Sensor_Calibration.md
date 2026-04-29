# Sensor Calibration Guide

## DHT22 — Temperature & Humidity

The DHT22 is factory calibrated. No manual calibration needed.

**Accuracy:** ±0.5°C temperature, ±2-5% humidity
**Tips:**
- Mount in shade, away from direct sunlight
- Keep at least 20cm from heat sources
- Wait 2 seconds between readings (library handles this)

---

## Capacitive Soil Moisture Sensor

The capacitive sensor outputs analog voltage. You must calibrate for your specific soil.

### Calibration Steps:

1. **Dry reading** — Hold sensor in open air for 30 seconds. Note ADC value → this is `SOIL_DRY`
2. **Wet reading** — Submerge sensor tip in water for 30 seconds. Note ADC value → this is `SOIL_WET`
3. Update `configs.h`:
```cpp
#define SOIL_DRY  3200  // Replace with your dry ADC value
#define SOIL_WET  1400  // Replace with your wet ADC value
```

**Typical values (ESP32 12-bit ADC):**
- Dry air: ~3100–3300
- Dry soil: ~2500–2800
- Moist soil: ~1800–2200
- Saturated: ~1200–1500

---

## BH1750 — Light Sensor

The BH1750 is factory calibrated for lux measurements.

**Accuracy:** ±20%
**Modes available:**
- `CONTINUOUS_HIGH_RES_MODE` — 1 lux resolution (used in this project)
- `CONTINUOUS_LOW_RES_MODE` — 4 lux resolution (faster)

**No calibration needed.** Just confirm I2C address:
- Default: `0x23` (ADDR pin LOW)
- Alternate: `0x5C` (ADDR pin HIGH)

---

## Relay Module

The relay is digital (ON/OFF) — no calibration needed.

**Wiring:**
- IN → ESP32 GPIO 26
- VCC → 5V
- GND → GND
- COM + NO → Pump circuit

**Logic:** `HIGH` = pump ON, `LOW` = pump OFF
