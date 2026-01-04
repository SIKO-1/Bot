import json
import os

DB_FILE = "database.json"

def load_db():
    """تحميل البيانات من الملف فوراً"""
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)
        return {}
    with open(DB_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            return {}

def save_db(data):
    """حفظ البيانات في الملف وإغلاقه فوراً"""
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def get_user(user_id):
    """جلب بيانات المستخدم بالكامل"""
    db = load_db()
    uid = str(user_id)
    if uid not in db:
        db[uid] = {"gold": 0, "messages": 0, "rank": "مواطن", "banned": False}
        save_db(db)
    return db[uid]

def update_user(user_id, data):
    """تحديث أي معلومة وحفظها"""
    db = load_db()
    uid = str(user_id)
    if uid not in db:
        db[uid] = {"gold": 0, "messages": 0, "rank": "مواطن", "banned": False}
    db[uid].update(data)
    save_db(db)

# --- الدوال المطلوبة لأوامر الذهب والفلوس ---

def get_user_gold(user_id):
    """هذه هي الدالة التي كانت ناقصة وتسببت بالخطأ"""
    user = get_user(user_id)
    return user.get("gold", 0)

def update_user_gold(user_id, amount):
    """تعديل الذهب مع ضمان الحفظ الأبدي"""
    db = load_db()
    uid = str(user_id)
    if uid not in db:
        db[uid] = {"gold": 0, "messages": 0}
    
    db[uid]["gold"] = db[uid].get("gold", 0) + amount
    save_db(db)

def increment_messages(user_id):
    """زيادة عداد الرسائل في كل حركة"""
    db = load_db()
    uid = str(user_id)
    if uid not in db:
        db[uid] = {"gold": 0, "messages": 0}
    db[uid]["messages"] = db[uid].get("messages", 0) + 1
    save_db(db)

# --- دوال نظام الروح (إحصائيات حقيقية) ---

def get_total_users_count():
    return len(load_db())

def get_banned_users_count():
    db = load_db()
    return len([u for u in db.values() if u.get("banned") == True])

def get_total_messages():
    db = load_db()
    return sum([u.get("messages", 0) for u in db.values()])
