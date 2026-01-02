import os
from pymongo import MongoClient
from dotenv import load_dotenv

# تحميل الإعدادات
load_dotenv()

# --- إعداد الاتصال بالسحابة ---
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

# --- الدوال المطلوبة لملفات الهدايا والمتجر ---

def get_user(user_id):
    """جلب بيانات المستخدم الكاملة (مطلوبة لـ cmd_gift)"""
    if collection is None: return None
    return collection.find_one({"user_id": user_id})

def update_user(user_id, data):
    """تحديث بيانات المستخدم بشكل عام"""
    if collection is None: return
    collection.update_one({"user_id": user_id}, {"$set": data}, upsert=True)

def get_user_gold(user_id):
    """جلب الذهب"""
    user = get_user(user_id)
    return user.get("gold", 0) if user else 0

def update_user_gold(user_id, amount):
    """تعديل الذهب (إضافة أو خصم)"""
    if collection is None: return
    collection.update_one(
        {"user_id": user_id},
        {"$inc": {"gold": amount}},
        upsert=True
    )

def add_item_to_inventory(user_id, item_name):
    """إضافة غرض للمعرض"""
    if collection is None: return
    collection.update_one(
        {"user_id": user_id},
        {"$push": {"inventory": item_name}},
        upsert=True
    )

def get_user_inventory(user_id):
    """جلب ممتلكات المعرض"""
    user = get_user(user_id)
    if user and "inventory" in user:
        return user["inventory"]
    return []
