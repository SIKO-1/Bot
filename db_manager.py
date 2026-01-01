import json
import os

DB_FILE = "/app/data/users_data.json"

def load_data():
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    if not os.path.exists(DB_FILE): return {}
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f: return json.load(f)
    except: return {}

def save_data(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def get_user(user_id):
    data = load_data()
    user_id = str(user_id)
    if user_id not in data:
        data[user_id] = {"balance": 0, "rank": "عضو", "last_gift": None}
        save_data(data)
    return data[user_id]

def update_user(user_id, key, value):
    data = load_data()
    data[str(user_id)][key] = value
    save_data(data)
