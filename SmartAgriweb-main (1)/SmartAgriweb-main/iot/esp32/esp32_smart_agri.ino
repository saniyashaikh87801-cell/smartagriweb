/*
 * ═══════════════════════════════════════════════════
 *  SmartAgriWeb — ESP32 IoT Sensor Node
 *  Sensors : DHT22 (Temp + Humidity)
 *             Capacitive Soil Moisture Sensor
 *             BH1750 (Light Lux)
 *  Output  : POST to Flask /api/sensors/ingest
 * ═══════════════════════════════════════════════════
 */

#include "configs.h"
#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>
#include <Wire.h>
#include <BH1750.h>
#include <ArduinoJson.h>

// ── Pin Definitions ──────────────────────────────
#define DHT_PIN         4      // DHT22 data pin
#define DHT_TYPE        DHT22
#define SOIL_PIN        34     // Analog pin for soil moisture
#define RELAY_PIN       26     // Irrigation pump relay
#define STATUS_LED      2      // Built-in LED

// ── Calibration Values ───────────────────────────
#define SOIL_DRY        3200   // Raw ADC value when dry
#define SOIL_WET        1400   // Raw ADC value when wet (in water)

// ── Timing ───────────────────────────────────────
#define SEND_INTERVAL   30000  // ms — send data every 30 seconds

// ── Objects ──────────────────────────────────────
DHT    dht(DHT_PIN, DHT_TYPE);
BH1750 lightMeter;

unsigned long lastSendTime = 0;

// ══════════════════════════════════════════════════
void setup() {
  Serial.begin(115200);
  Serial.println("\n🌱 SmartAgriWeb ESP32 Starting...");

  pinMode(RELAY_PIN,  OUTPUT);
  pinMode(STATUS_LED, OUTPUT);
  digitalWrite(RELAY_PIN, LOW);   // Pump off by default

  // Init sensors
  dht.begin();
  Wire.begin();
  if (lightMeter.begin(BH1750::CONTINUOUS_HIGH_RES_MODE)) {
    Serial.println("✅ BH1750 light sensor OK");
  } else {
    Serial.println("⚠️  BH1750 not found, using 0 lux");
  }

  // Connect WiFi
  connectWiFi();
}

// ══════════════════════════════════════════════════
void loop() {
  // Reconnect if needed
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("⚠️ WiFi lost — reconnecting...");
    connectWiFi();
  }

  unsigned long now = millis();
  if (now - lastSendTime >= SEND_INTERVAL) {
    lastSendTime = now;
    readAndSend();
  }
}

// ══════════════════════════════════════════════════
void connectWiFi() {
  Serial.printf("📡 Connecting to %s ", WIFI_SSID);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
  }
  if (WiFi.status() == WL_CONNECTED) {
    Serial.printf("\n✅ Connected! IP: %s\n", WiFi.localIP().toString().c_str());
    digitalWrite(STATUS_LED, HIGH);
  } else {
    Serial.println("\n❌ WiFi connection failed. Will retry.");
    digitalWrite(STATUS_LED, LOW);
  }
}

// ══════════════════════════════════════════════════
void readAndSend() {
  // ── Read DHT22 ──
  float temperature = dht.readTemperature();
  float humidity    = dht.readHumidity();

  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("❌ DHT22 read failed");
    return;
  }

  // ── Read Soil Moisture ──
  int rawSoil    = analogRead(SOIL_PIN);
  int soilPct    = map(rawSoil, SOIL_DRY, SOIL_WET, 0, 100);
  soilPct        = constrain(soilPct, 0, 100);

  // ── Read Light ──
  float lux = lightMeter.readLightLevel();
  if (lux < 0) lux = 0;

  // ── Print to Serial ──
  Serial.printf("🌡 Temp: %.1f°C  💧 Hum: %.0f%%  🌱 Soil: %d%%  ☀️ Lux: %.0f\n",
                temperature, humidity, soilPct, lux);

  // ── Send to Flask API ──
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    String url = String(SERVER_URL) + "/api/sensors/ingest";
    http.begin(url);
    http.addHeader("Content-Type", "application/json");

    // Build JSON payload
    StaticJsonDocument<200> doc;
    doc["temperature"]   = round(temperature * 10) / 10.0;
    doc["humidity"]      = (int)humidity;
    doc["soil_moisture"] = soilPct;
    doc["light_lux"]     = (int)lux;

    String payload;
    serializeJson(doc, payload);

    int httpCode = http.POST(payload);
    if (httpCode == 201) {
      Serial.println("✅ Data sent to server");
      blinkLED(2);
    } else {
      Serial.printf("⚠️ Server returned: %d\n", httpCode);
    }
    http.end();
  }

  // ── Auto Irrigation Logic ──
  if (soilPct < 25) {
    Serial.println("🚿 Auto-irrigating: soil too dry!");
    digitalWrite(RELAY_PIN, HIGH);   // Turn pump ON
    delay(5000);                      // Run 5 seconds
    digitalWrite(RELAY_PIN, LOW);    // Turn pump OFF
  }
}

// ══════════════════════════════════════════════════
void blinkLED(int times) {
  for (int i = 0; i < times; i++) {
    digitalWrite(STATUS_LED, LOW);
    delay(100);
    digitalWrite(STATUS_LED, HIGH);
    delay(100);
  }
}
