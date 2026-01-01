import json
import os

# اسم الملف الذي سيتم تخزين البيانات فيه بصيغة JSON
DB_FILE = "users_data.json"

def load_data():
    """تحميل بيانات المستخدمين من الملف"""
    if not os.path.exists(DB_FILE):
        return {}
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_data(data):
    """حفظ البيانات الحالية في الملف"""
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def get_user(user_id):
    """جلب بيانات مستخدم معين أو إنشاء بيانات جديدة له إذا لم تكن موجودة"""
    data = load_data()
    uid = str(user_id)
    if uid not in data:
        # الإعدادات الافتراضية لأي شخص يبدأ في الإمبراطورية
        data[uid] = {
            "points": 0,      # النقاط التي يجمعها
            "level": 1,       # المستوى الحالي
            "rank": "مبتدئ",    # الرتبة الأولية
            "exp": 0          # الخبرة (عدد الرسائل المرسلة)
        }
        save_data(data)
    return data[uid]
