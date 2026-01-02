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

# --- جلب بيانات المستخدم (معدلة لمنع التصفير) ---
def get_user(user_id):
    data = load_data()
    user_id = str(user_id)
    
    # إذا كان المستخدم موجوداً، نرجعه فوراً ولا نلمس بياناته
    if user_id in data:
        # نأكد وجود المفاتيح الجديدة لو كانت مفقودة (مثل xp أو rank)
        user = data[user_id]
        changed = False
        defaults = {"balance": 0, "level": 1, "xp": 0, "inventory": [], "rank": "مبتدئ", "bio": "لا يوجد"}
        for key, val in defaults.items():
            if key not in user:
                user[key] = val
                changed = True
        if changed:
            save_data(data)
        return user
    
    # فقط للمستخدم الجديد، ننشئ بياناته الافتراضية
    data[user_id] = {
        "balance": 0, 
        "level": 1, 
        "xp": 0, 
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
        get_user(user_id) # لإنشائه لو لم يكن موجوداً
        data = load_data()
    data[user_id][key] = value
    save_data(data)

# --- دوال الاقتصاد والمستوى (التي تطلبها الملفات الأخرى) ---

def get_balance(user_id):
    user = get_user(user_id)
    return user.get('balance', 0)

def update_balance(user_id, amount):
    user = get_user(user_id)
    new_balance = user.get('balance', 0) + amount
    update_user(user_id, 'balance', new_balance)

def update_level(user_id, amount):
    user = get_user(user_id)
    new_level = user.get('level', 1) + amount
    update_user(user_id, 'level', new_level)

def update_xp(user_id, amount):
    user = get_user(user_id)
    xp = user.get('xp', 0) + amount
    current_lvl = user.get('level', 1)
    
    # معادلة الصعوبة: تزداد كلما زاد المستوى
    difficulty = (current_lvl // 50) + 1
    needed_xp = current_lvl * (10 * difficulty)
    
    if xp >= needed_xp:
        new_lvl = current_lvl + 1
        update_user(user_id, 'level', new_lvl)
        update_user(user_id, 'xp', 0)
        return True, new_lvl
    
    update_user(user_id, 'xp', xp)
    return False, current_lvl

# --- دوال المعرض والرتب ---

def add_to_inventory(user_id, item_name):
    user = get_user(user_id)
    inv = user.get('inventory', [])
    inv.append(item_name)
    update_user(user_id, 'inventory', inv)

def get_inventory(user_id):
    user = get_user(user_id)
    return user.get('inventory', [])

def remove_from_inventory(user_id, item_name):
    user = get_user(user_id)
    inv = user.get('inventory', [])
    if item_name in inv:
        inv.remove(item_name)
        update_user(user_id, 'inventory', inv)
        return True
    return False

def get_rank(user_id):
    user = get_user(user_id)
    return user.get('rank', "مبتدئ")

def set_rank(user_id, rank_name):
    update_user(user_id, 'rank', rank_name)
