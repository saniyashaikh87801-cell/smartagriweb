/*
 * configs.h — SmartAgriWeb ESP32 Configuration
 * ─────────────────────────────────────────────
 * Edit these values before flashing to your ESP32
 */

#ifndef CONFIGS_H
#define CONFIGS_H

// ── WiFi Credentials ──────────────────────────────
#define WIFI_SSID       "YOUR_WIFI_SSID"
#define WIFI_PASSWORD   "YOUR_WIFI_PASSWORD"

// ── Flask Server URL ──────────────────────────────
// Use your PC's local IP if running locally
// e.g., "http://192.168.1.100:5500"
#define SERVER_URL      "http://192.168.1.100:5500"

// ── Device ID ─────────────────────────────────────
#define DEVICE_ID       "ESP32-FIELD-01"

#endif
