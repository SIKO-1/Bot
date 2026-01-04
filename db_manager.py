import json
import os

DB_FILE = "database.json"

def load_db():
    """تحميل البيانات من الملف الداخلي"""
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            return {}

def save_db(data):
    """حفظ البيانات في الملف"""
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def get_user(user_id):
    """جلب بيانات المستخدم بالكامل"""
    db = load_db()
    uid = str(user_id)
    if uid not in db:
        # إنشاء سجل جديد للمواطن إذا لم يوجد
        db[uid] = {"gold": 0, "messages": 0, "rank": "مواطن", "banned": False}
        save_db(db)
    return db.get(uid)

def update_user(user_id, data):
    """تحديث بيانات المستخدم (مثل الحظر أو الرتبة)"""
    db = load_db()
    uid = str(user_id)
    if uid not in db:
        db[uid] = {"gold": 0, "messages": 0, "rank": "مواطن", "banned": False}
    db[uid].update(data)
    save_db(db)

def get_user_gold(user_id):
    """جلب رصيد الذهب الحالي"""
    user = get_user(user_id)
    return user.get("gold", 0)

def update_user_gold(user_id, amount):
    """تعديل الذهب (زيادة أو نقصان) مع الحفظ الفوري"""
    db = load_db()
    uid = str(user_id)
    if uid not in db:
        db[uid] = {"gold": 0, "messages": 0}
    
    db[uid]["gold"] = db[uid].get("gold", 0) + amount
    save_db(db)

def increment_messages(user_id):
    """زيادة عداد الرسائل لضمان حفظ النشاط"""
    db = load_db()
    uid = str(user_id)
    if uid not in db:
        db[uid] = {"gold": 0, "messages": 0}
    db[uid]["messages"] = db[uid].get("messages", 0) + 1
    save_db(db)

# --- دوال نظام الروح الإحصائية ---

def get_total_users_count():
    """عدد النفوس المسجلة"""
    db = load_db()
    return len(db)

def get_banned_users_count():
    """عدد المنفيين"""
    db = load_db()
    return len([u for u in db.values() if u.get("banned") == True])

def get_total_messages():
    """إجمالي صرخات الرعايا"""
    db = load_db()
    return sum([u.get("messages", 0) for u in db.values()])
