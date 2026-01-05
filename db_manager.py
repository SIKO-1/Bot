# ملف: db_manager.py
import time
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# ======================
# إعداد MongoDB
# ======================
MONGO_URI = "mongodb+srv://wpee923_db_user:08520852KR@cluster0.nzjd5gc.mongodb.net/?retryWrites=true&w=majority"
DB_NAME = "imperial_bot"

try:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    users_collection = db["users"]
    print("✅ MongoDB متصل بنجاح!")
except ConnectionFailure:
    print("❌ فشل الاتصال بـ MongoDB")

# ======================
# دوال المستخدم
# ======================
def get_user(uid: int) -> dict:
    user = users_collection.find_one({"uid": uid})
    if not user:
        # إنشاء مستخدم جديد
        user_data = {
            "uid": uid,
            "gold": 0,
            "bank": 0,
            "inventory": [],
            "last_gift": 0
        }
        users_collection.insert_one(user_data)
        return user_data
    return user

# ======================
# الذهب العادي
# ======================
def get_user_gold(uid: int) -> int:
    return get_user(uid).get("gold", 0)

def update_user_gold(uid: int, amount: int) -> int:
    user = get_user(uid)
    new_gold = max(user.get("gold", 0) + amount, 0)
    users_collection.update_one({"uid": uid}, {"$set": {"gold": new_gold}})
    return new_gold

# ======================
# البنك
# ======================
def get_user_bank(uid: int) -> int:
    return get_user(uid).get("bank", 0)

def update_user_bank(uid: int, amount: int) -> int:
    user = get_user(uid)
    new_bank = max(user.get("bank", 0) + amount, 0)
    users_collection.update_one({"uid": uid}, {"$set": {"bank": new_bank}})
    return new_bank

def get_total_bank() -> int:
    return sum(user.get("bank", 0) for user in users_collection.find())

# ======================
# الهدايا اليومية
# ======================
def can_take_gift(uid: int) -> bool:
    user = get_user(uid)
    last = user.get("last_gift", 0)
    return time.time() - last >= 86400  # 24 ساعة

def take_gift(uid: int, amount: int = 100) -> int | None:
    if can_take_gift(uid):
        new_gold = update_user_gold(uid, amount)
        users_collection.update_one({"uid": uid}, {"$set": {"last_gift": time.time()}})
        return new_gold
    return None

# ======================
# المخزون / Inventory
# ======================
def get_inventory(uid: int) -> list:
    return get_user(uid).get("inventory", [])

def add_to_inventory(uid: int, item: str, quantity: int = 1) -> None:
    user = get_user(uid)
    inventory = user.get("inventory", [])
    inventory.extend([item] * quantity)
    users_collection.update_one({"uid": uid}, {"$set": {"inventory": inventory}})

def remove_from_inventory(uid: int, item: str, quantity: int = 1) -> bool:
    user = get_user(uid)
    inventory = user.get("inventory", [])
    count = 0
    new_inventory = []
    for i in inventory:
        if i == item and count < quantity:
            count += 1
            continue
        new_inventory.append(i)
    users_collection.update_one({"uid": uid}, {"$set": {"inventory": new_inventory}})
    return count == quantity

# ======================
# المستوى (كل 500 ذهب = +10 مستويات)
# ======================
def get_user_level(uid: int) -> int:
    gold = get_user_gold(uid)
    return (gold // 500) * 10
