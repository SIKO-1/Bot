import json
import os

# المسار الجديد المرتبط بـ Volume ريلوي لضمان عدم ضياع البيانات
DB_FILE = "/app/data/users_data.json"

def load_data():
    """تحميل البيانات من الملف، وإنشاء ملف جديد إذا لم يكن موجوداً"""
    # التأكد من وجود المجلد أولاً لتجنب الأخطاء
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    
    if not os.path.exists(DB_FILE):
        return {}
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

def save_data(data):
    """حفظ البيانات في الملف بشكل آمن"""
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"خطأ في حفظ البيانات: {e}")

def get_user(user_id):
    """جلب بيانات مستخدم معين مع القيم الافتراضية"""
    data = load_data()
    user_id = str(user_id)
    if user_id not in data:
        data[user_id] = {
            "balance": 0,
            "rank": "عضو",
            "last_gift": None,  # لتخزين وقت آخر هدية
            "inventory": []      # لتخزين المشتريات
        }
        save_data(data)
    return data[user_id]

def update_user(user_id, key, value):
    """تحديث معلومة محددة للمستخدم (مثل الرصيد أو الرتبة)"""
    data = load_data()
    user_id = str(user_id)
    if user_id not in data:
        get_user(user_id)
        data = load_data()
    
    data[user_id][key] = value
    save_data(data)
