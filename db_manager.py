import json
import os

# تحديد المسار المطلق للملف لضمان عدم ضياعه في المجلدات المؤقتة
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
        # الحفظ بطريقة الكتابة المباشرة والآمنة
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            f.flush()
            os.fsync(f.fileno())
    except Exception as e:
        print(f"Error saving: {e}")

def get_user(user_id):
    data = load_data()
    uid = str(user_id)
    if uid not in data:
        data[uid] = {"balance": 0, "inventory": [], "rank": "مبتدئ", "bio": "لا يوجد"}
        save_data(data)
    return data[uid]

def update_balance(user_id, amount):
    data = load_data()
    uid = str(user_id)
    user = get_user(uid)
    data[uid]["balance"] = user.get("balance", 0) + amount
    save_data(data)

def set_rank(user_id, rank_name):
    data = load_data()
    uid = str(user_id)
    if uid in data:
        data[uid]["rank"] = rank_name
        save_data(data)
