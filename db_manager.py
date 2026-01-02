import json
import os

DB_FILE = "database.json"

# --- دالة تحميل البيانات بأمان ---
def load_data():
    if not os.path.exists(DB_FILE):
        return {}
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ خطأ في قراءة القاعدة: {e}")
        return {}

# --- دالة الحفظ القسري (تمنع التصفير نهائياً) ---
def save_data(data):
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            f.flush() # تفريغ الذاكرة المؤقتة في الملف
            os.fsync(f.fileno()) # إجبار نظام التشغيل على الكتابة في القرص الصلب فوراً
    except Exception as e:
        print(f"❌ خطأ فادح في الحفظ: {e}")

# --- جلب بيانات المستخدم بذكاء ---
def get_user(user_id):
    data = load_data()
    uid = str(user_id)
    
    # إذا كان المستخدم موجوداً، نحدث النواقص فقط ولا نصفر القديم
    if uid in data:
        user = data[uid]
        updated = False
        # التأكد من وجود كل المفاتيح (لحماية البيانات القديمة)
        defaults = {
            "balance": 0, 
            "level": 1, 
            "xp": 0, 
            "inventory": [], 
            "rank": "مبتدئ", 
            "bio": "لا يوجد بايو"
        }
        for key, val in defaults.items():
            if key not in user:
                user[key] = val
                updated = True
        if updated:
            save_data(data)
        return user
    
    # للمستخدم الجديد كلياً
    data[uid] = {
        "balance": 0, 
        "level": 1, 
        "xp": 0, 
        "inventory": [], 
        "rank": "مبتدئ", 
        "bio": "لا يوجد بايو"
    }
    save_data(data)
    return data[uid]

# --- تحديث البيانات بدقة ---
def update_user(user_id, key, value):
    data = load_data()
    uid = str(user_id)
    if uid not in data:
        get_user(uid)
        data = load_data()
    
    data[uid][key] = value
    save_data(data)

# --- دوال الاقتصاد والمستوى الملكية ---

def get_balance(user_id):
    user = get_user(user_id)
    return user.get('balance', 0)

def update_balance(user_id, amount):
    user = get_user(user_id)
    new_bal = user.get('balance', 0) + amount
    update_user(user_id, 'balance', new_bal)

def update_level(user_id, amount):
    user = get_user(user_id)
    new_lvl = user.get('level', 1) + amount
    update_user(user_id, 'level', new_lvl)

def update_xp(user_id, amount):
    user = get_user(user_id)
    xp = user.get('xp', 0) + amount
    lvl = user.get('level', 1)
    
    # نظام الصعوبة الإمبراطوري: يزداد الثقل كل 50 لفل
    difficulty = (lvl // 50) + 1
    needed_xp = lvl * (10 * difficulty)
    
    if xp >= needed_xp:
        new_lvl = lvl + 1
        update_user(user_id, 'level', new_lvl)
        update_user(user_id, 'xp', 0)
        return True, new_lvl
    
    update_user(user_id, 'xp', xp)
    return False, lvl

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
