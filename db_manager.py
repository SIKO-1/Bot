import os
from pymongo import MongoClient
from dotenv import load_dotenv

# تحميل الإعدادات
load_dotenv()

# الاتصال بقاعدة البيانات (تأكد من وجود MONGO_URL في إعدادات الاستضافة)
MONGO_URL = os.getenv('MONGO_URL')
client = MongoClient(MONGO_URL)
db = client['EmpireBotDB']  # اسم قاعدة البيانات
collection = db['users']    # اسم جدول المستخدمين

def get_user_gold(user_id):
    """جلب رصيد الذهب"""
    user = collection.find_one({"user_id": user_id})
    if user:
        return user.get("gold", 0)
    return 0

def update_user_gold(user_id, amount):
    """تحديث الذهب (إضافة أو خصم)"""
    collection.update_one(
        {"user_id": user_id},
        {"$inc": {"gold": amount}},
        upsert=True
    )

def add_item_to_inventory(user_id, item_name):
    """إضافة أداة للمعرض بعد الشراء"""
    collection.update_one(
        {"user_id": user_id},
        {"$push": {"inventory": item_name}},
        upsert=True
    )

def get_user_inventory(user_id):
    """جلب ممتلكات المعرض"""
    user = collection.find_one({"user_id": user_id})
    if user and "inventory" in user:
        return user["inventory"]
    return []
