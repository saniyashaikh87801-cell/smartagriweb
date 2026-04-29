from models.crops_model import CROPS
import json, os

# Load irrigation rules
_RULES_PATH = os.path.join(os.path.dirname(__file__), "..", "datasets", "irrigation_rules.json")
def _load_rules():
    try:
        with open(_RULES_PATH) as f:
            return json.load(f)
    except:
        return {}
IRRIGATION_RULES = _load_rules()


class CropRecommender:

    SEASON_CROPS = {
        "Summer":      ["tomato","corn","cucumber","pepper","watermelon","mango","banana"],
        "Winter":      ["wheat","spinach","garlic","carrot"],
        "Spring":      ["potato","onion","strawberry","carrot","soybean"],
        "Monsoon":     ["rice","sugarcane","banana"],
        "Cool Season": ["spinach","carrot","potato","wheat"],
        "Fall":        ["garlic","onion","potato","carrot"],
        "Year-round":  ["banana","sugarcane"],
    }

    @staticmethod
    def recommend(temperature=28, humidity=60, soil_moisture=45,
                  soil_type="loamy", season="Summer"):
        """
        Score each crop against current conditions.
        Returns top 5 with score and reason.
        """
        season_keys = CropRecommender.SEASON_CROPS.get(season, [])
        results = []

        for key, crop in CROPS.items():
            score = 0
            reasons = []

            # Season match
            if key in season_keys:
                score += 40
                reasons.append(f"Ideal for {season}")

            # Temperature match (rough heuristic from crop season)
            crop_season = crop.get("season", "")
            if season.lower() in crop_season.lower() or crop_season == "Year-round":
                score += 20

            # Soil moisture match via weekly_water hint
            avg_water = sum(crop.get("weekly_water", [30]*7)) / 7
            if soil_moisture >= 40 and avg_water >= 40:
                score += 15
                reasons.append("Good soil moisture match")
            elif soil_moisture < 40 and avg_water < 30:
                score += 15
                reasons.append("Low-water crop suits dry conditions")

            # Humidity
            if humidity >= 55:
                if key in ["rice","banana","sugarcane","cucumber"]:
                    score += 10
                    reasons.append("Thrives in humid conditions")
            else:
                if key in ["wheat","garlic","onion","carrot"]:
                    score += 10
                    reasons.append("Suits lower humidity")

            if score > 0:
                results.append({
                    "key":      key,
                    "name":     crop["name"],
                    "icon":     crop["icon"],
                    "category": crop["category"],
                    "score":    score,
                    "reasons":  reasons[:2],
                    "days":     crop["days"],
                    "yield":    crop["yield"],
                })

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:5]
