import json, os

DB_FILE = "users_data.json"

def load_data():
    try:
        if not os.path.exists(DB_FILE): return {}
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error Loading DB: {e}")
        return {}

def save_data(data):
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"❌ Error Saving DB: {e}")

def get_user(user_id):
    data = load_data()
    uid = str(user_id)
    if uid not in data:
        data[uid] = {"points": 0, "level": 1, "rank": "مبتدئ", "exp": 0}
        save_data(data)
    return data[uid]
