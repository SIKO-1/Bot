import json
import os

DB_FILE = "users_data.json"

def load_data():
    if not os.path.exists(DB_FILE):
        return {}
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_mode=False)

def get_user(user_id):
    data = load_data()
    user_id = str(user_id)
    if user_id not in data:
        data[user_id] = {
            "points": 0,
            "level": 1,
            "exp": 0,
            "rank": "متدرب",
            "last_gift_time": None
        }
        save_data(data)
    return data[user_id]
