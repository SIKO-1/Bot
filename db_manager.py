import json
import os

DB_FILE = "database.json"

def load_db():
    """تحميل البيانات من الملف فوراً لضمان أحدث نسخة"""
    if not os.path.exists(DB_FILE):
        # إذا الملف مو موجود ننشئه فاضي
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)
        return {}
    
    with open(DB_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            return data
        except:
            return {}

def save_db(data):
    """حفظ البيانات في الملف وإغلاقه فوراً لضمان عدم الضياع"""
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def get_user(user_id):
    """جلب بيانات المواطن، وإذا مو موجود نسجله فوراً"""
    db = load_db()
    uid = str(user_id)
    if uid not in db:
        db[uid] = {"gold": 0, "messages": 0, "rank": "مواطن", "banned": False}
        save_db(db) # نحفظه فوراً في الملف
    return db[uid]

def update_user(user_id, data):
    """تحديث أي معلومة (ذهب، رتبة، حظر) وحفظها للأبد"""
    db = load_db()
    uid = str(user_id)
    if uid not in db:
        db[uid] = {"gold": 0, "messages": 0, "rank": "مواطن", "banned": False}
    
    db[uid].update(data)
    save_db(db) # الحفظ الفوري

def update_user_gold(user_id, amount):
    """إضافة أو خصم الذهب مع ضمان الحفظ"""
    db = load_db()
    uid = str(user_id)
    if uid not in db:
        db[uid] = {"gold": 0, "messages": 0}
    
    # تأكدنا أننا نستخدم مفتاح "gold" الموحد
    current_gold = db[uid].get("gold", 0)
    db[uid]["gold"] = current_gold + amount
    save_db(db)

def increment_messages(user_id):
    """تحديث عداد الرسائل في كل مرة يرسل فيها الشخص رسالة"""
    db = load_db()
    uid = str(user_id)
    if uid not in db:
        db[uid] = {"gold": 0, "messages": 0}
    
    db[uid]["messages"] = db[uid].get("messages", 0) + 1
    save_db(db)

# --- دوال نظام الروح (بيانات حقيقية من الملف) ---
def get_total_users_count():
    return len(load_db())

def get_banned_users_count():
    db = load_db()
    return len([u for u in db.values() if u.get("banned") == True])

def get_total_messages():
    db = load_db()
    return sum([u.get("messages", 0) for u in db.values()])
