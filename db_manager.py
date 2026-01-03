import os
from pymongo import MongoClient
from dotenv import load_dotenv

# تحميل الإعدادات
load_dotenv()

# --- إعداد الاتصال بالسحابة ---
# تأكد أن MONGO_URL موجود في متغيرات البيئة بـ Railway
MONGO_URL = os.getenv('MONGO_URL')

try:
    client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
    db = client['EmpireBotDB']
    collection = db['users']
    client.admin.command('ping')
    print("✅ تم الاتصال بسحابة MongoDB بنجاح!")
except Exception as e:
    print(f"❌ فشل الاتصال بالسحابة: {e}")
    collection = None

# --- 💠 دوال الإمبراطورية الأساسية 💠 ---

def get_user(user_id):
    """جلب بيانات المستخدم الكاملة (مهمة لحل خطأ NoneType)"""
    if collection is None: return None
    return collection.find_one({"user_id": user_id})

def update_user(user_id, data):
    """تحديث أي بيانات للمستخدم (مثل وقت الهدية أو المعرض)"""
    if collection is None: return
    # استخدام $set لتحديث الحقول المحددة فقط دون مسح البقية
    collection.update_one({"user_id": user_id}, {"$set": data}, upsert=True)

def get_user_gold(user_id):
    """جلب الذهب الحالي للمستخدم (حل مشكلة الرصيد 0)"""
    user = get_user(user_id)
    # نستخدم حقل gold حصراً ليتوافق مع المتجر والهدايا [cite: 2026-01-02]
    return user.get("gold", 0) if user else 0

def update_user_gold(user_id, amount):
    """تعديل الذهب (إضافة أو خصم) بشكل آمن"""
    if collection is None: return
    # استخدام $inc لزيادة أو تنقيص القيمة الحالية بدلاً من استبدالها
    collection.update_one(
        {"user_id": user_id},
        {"$inc": {"gold": amount}},
        upsert=True
    )

def add_item_to_inventory(user_id, item_name):
    """إضافة غرض للممتلكات (درع، عفو، الخ)"""
    if collection is None: return
    collection.update_one(
        {"user_id": user_id},
        {"$push": {"inventory": item_name}},
        upsert=True
    )

def get_user_inventory(user_id):
    """عرض الممتلكات في المعرض"""
    user = get_user(user_id)
    if user and "inventory" in user:
        return user["inventory"]
    return []
