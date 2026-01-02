import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "database.json")

def load_data():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w", encoding="utf-8") as f:
            f.write("{}")
        return {}
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            content = f.read()
            return json.loads(content) if content else {}
    except:
        return {}

def save_data(data):
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            f.flush()
            os.fsync(f.fileno())
    except Exception as e:
        print(f"Error in Saving: {e}")

def get_user(user_id):
    data = load_data()
    uid = str(user_id)
    if uid not in data:
        data[uid] = {
            "balance": 0, 
            "inventory": [], 
            "rank": "مبتدئ", 
            "bio": "لا يوجد بايو"
        }
        save_data(data)
    return data[uid]

# --- الدالة المطلوبة لملف الهدية (update_user) ---
def update_user(user_id, key, value):
    data = load_data()
    uid = str(user_id)
    if uid not in data:
        get_user(uid)
        data = load_data()
    data[uid][key] = value
    save_data(data)

# --- الدوال المطلوبة لملف الرصيد والفلوس ---
def get_balance(user_id):
    user = get_user(user_id)
    return user.get('balance', 0)

def update_balance(user_id, amount):
    user = get_user(user_id)
    new_bal = user.get('balance', 0) + amount
    update_user(user_id, 'balance', new_bal)
