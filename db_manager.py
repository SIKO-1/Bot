import json
import os

DB_FILE = "database.json"

# --- دالة تحميل البيانات ---
def load_data():
    if not os.path.exists(DB_FILE):
        return {}
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

# --- دالة حفظ البيانات ---
def save_data(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# --- جلب بيانات المستخدم ---
def get_user(user_id):
    data = load_data()
    user_id = str(user_id)
    if user_id not in data:
        data[user_id] = {
            "balance": 0, 
            "inventory": [], 
            "rank": "مبتدئ", 
            "bio": "لا يوجد بايو"
        }
        save_data(data)
    return data[user_id]

# --- تحديث قيمة معينة للمستخدم ---
def update_user(user_id, key, value):
    data = load_data()
    user_id = str(user_id)
    if user_id not in data:
        get_user(user_id)
        data = load_data()
    data[user_id][key] = value
    save_data(data)

# --- دوال الاقتصاد الأساسية ---

def get_balance(user_id):
    user = get_user(user_id)
    return user.get('balance', 0)

def update_balance(user_id, amount):
    user = get_user(user_id)
    new_balance = user.get('balance', 0) + amount
    update_user(user_id, 'balance', new_balance)

# --- دوال المعرض والرتب ---

def add_to_inventory(user_id, item_name):
    user = get_user(user_id)
    inv = user.get('inventory', [])
    inv.append(item_name)
    update_user(user_id, 'inventory', inv)

def get_inventory(user_id):
    user = get_user(user_id)
    return user.get('inventory', [])

def get_rank(user_id):
    user = get_user(user_id)
    return user.get('rank', "مبتدئ")

def set_rank(user_id, rank_name):
    update_user(user_id, 'rank', rank_name)
