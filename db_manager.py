import os
from pymongo import MongoClient
from dotenv import load_dotenv

# تحميل الإعدادات من بيئة Railway
load_dotenv()

# الاتصال بقاعدة البيانات
MONGO_URL = os.getenv('MONGO_URL')
client = MongoClient(MONGO_URL)
db = client['EmpireBotDB']
collection = db['users']

def get_user(user_id):
    """جلب بيانات المستخدم أو إنشاء قاموس فارغ إذا لم يوجد"""
    return collection.find_one({"user_id": user_id}) or {}

def update_user(user_id, data):
    """تحديث البيانات العامة مثل وقت الهدية"""
    collection.update_one({"user_id": user_id}, {"$set": data}, upsert=True)

def get_user_gold(user_id):
    """جلب رصيد الذهب الحالي"""
    user = collection.find_one({"user_id": user_id})
    # نستخدم gold ليتوافق مع أسعار المتجر [cite: 2026-01-02]
    return user.get("gold", 0) if user else 0

def update_user_gold(user_id, amount):
    """إضافة الذهب فعلياً للسحابة (حل مشكلة الرصيد 0)"""
    # $inc تضمن إضافة الـ 500 فوق الرصيد الحالي ولا تمسحه
    collection.update_one(
        {"user_id": user_id},
        {"$inc": {"gold": amount}},
        upsert=True
    )
