import json
import os

DB_FILE = "users_data.json"

def load_data():
    if not os.path.exists(DB_FILE):
        return {}
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            content = f.read()
            return json.loads(content) if content else {}
    except Exception:
        return {}

def save_data(data):
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"❌ Error saving data: {e}")

def get_user(user_id):
    data = load_data()
    uid = str(user_id)
    if uid not in data:
        data[uid] = {
            "points": 0,
            "level": 1,
            "exp": 0,
            "rank": "متدرب",
            "last_gift_time": "2000-01-01T00:00:00" # تاريخ قديم جداً للسماح بالهدية فوراً
        }
        save_data(data)
    return data[uid]
