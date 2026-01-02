import os
from pymongo import MongoClient
from dotenv import load_dotenv

# تحميل المتغيرات من ملف .env أو إعدادات الاستضافة
load_dotenv()

# --- إعداد الاتصال بالسحابة ---
MONGO_URL = os.getenv('MONGO_URL')

try:
    # إعداد العميل مع مهلة زمنية 5 ثوانٍ لعدم تعليق البوت
    client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
    db = client['EmpireBotDB']
    collection = db['users']
    
    # اختبار الاتصال فوراً
    client.admin.command('ping')
    print("✅ تم الاتصال بسحابة MongoDB بنجاح!")
except Exception as e:
    print(f"❌ فشل الاتصال بالسحابة: {e}")
    # تعريف مجموعة وهمية لمنع انهيار الملفات الأخرى
    collection = None

# --- دوال إدارة الذهب (Gold) ---

def get_user_gold(user_id):
    """جلب رصيد الذهب للمستخدم"""
    if collection is None: return 0
    user = collection.find_one({"user_id": user_id})
    return user.get("gold", 0) if user else 0

def update_user_gold(user_id, amount):
    """تعديل الذهب (إضافة أو خصم)"""
    if collection is None: return
    collection.update_one(
        {"user_id": user_id},
        {"$inc": {"gold": amount}},
        upsert=True
    )

# --- دوال إدارة المعرض (Inventory) ---

def add_item_to_inventory(user_id, item_name):
    """إضافة غرض مشتري إلى معرض المستخدم"""
    if collection is None: return
    collection.update_one(
        {"user_id": user_id},
        {"$push": {"inventory": item_name}},
        upsert=True
    )

def get_user_inventory(user_id):
    """جلب قائمة ممتلكات المستخدم من المعرض"""
    if collection is None: return []
    user = collection.find_one({"user_id": user_id})
    if user and "inventory" in user:
        return user["inventory"]
    return []
