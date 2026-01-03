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
        # تم تصحيح الخطأ هنا بحذف الكلمة الخاطئة
        json.dump(data, f, ensure_ascii=False, indent=4)

def get_user(user_id):
    """جلب بيانات المستخدم"""
    db = load_db()
    return db.get(str(user_id), {})

def update_user(user_id, data):
    """تحديث بيانات المستخدم"""
    db = load_db()
    uid = str(user_id)
    if uid not in db:
        db[uid] = {}
    db[uid].update(data)
    save_db(db)

def get_user_gold(user_id):
    """جلب رصيد الذهب"""
    user = get_user(user_id)
    return user.get("gold", 0)

def update_user_gold(user_id, amount):
    """إضافة الذهب الحقيقي وتصحيح خطأ الـ 0"""
    db = load_db()
    uid = str(user_id)
    if uid not in db:
        db[uid] = {"gold": 0}
    
    # عملية الجمع الصحيحة
    db[uid]["gold"] = db[uid].get("gold", 0) + amount
    save_db(db)
