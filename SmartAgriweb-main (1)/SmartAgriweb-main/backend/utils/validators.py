def validate_sensor_payload(data: dict):
    errors = []
    if not isinstance(data.get("temperature"), (int, float)):
        errors.append("temperature must be a number")
    if not isinstance(data.get("humidity"), (int, float)):
        errors.append("humidity must be a number")
    if not isinstance(data.get("soil_moisture"), (int, float)):
        errors.append("soil_moisture must be a number")
    temp = data.get("temperature", 25)
    if not (-20 <= temp <= 60):
        errors.append("temperature out of valid range (-20 to 60°C)")
    hum = data.get("humidity", 50)
    if not (0 <= hum <= 100):
        errors.append("humidity must be 0–100%")
    soil = data.get("soil_moisture", 50)
    if not (0 <= soil <= 100):
        errors.append("soil_moisture must be 0–100%")
    return errors
