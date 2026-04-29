import json
import os

# ── Load full crop dataset from JSON ──
_DATASET_PATH = os.path.join(os.path.dirname(__file__), "..", "datasets", "crops_full_dataset.json")

def _load_crops():
    try:
        with open(_DATASET_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

CROPS = _load_crops()

class CropModel:

    @staticmethod
    def search(query: str):
        q = query.strip().lower()
        results = []
        for key, crop in CROPS.items():
            if q in crop["name"].lower() or q in crop["category"].lower():
                results.append({
                    "key":      key,
                    "name":     crop["name"],
                    "icon":     crop["icon"],
                    "category": crop["category"],
                    "days":     crop["days"],
                })
        return results

    @staticmethod
    def get(crop_key: str):
        crop = CROPS.get(crop_key.lower())
        if not crop:
            return None
        return {**crop, "key": crop_key.lower()}

    @staticmethod
    def all_keys():
        return list(CROPS.keys())

    @staticmethod
    def get_all():
        return [{**v, "key": k} for k, v in CROPS.items()]
