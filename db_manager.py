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
# دوال الذهب
# ======================
def get_user_gold(uid: int) -> int:
    user = users_collection.find_one({"uid": uid})
    if user:
        return user.get("gold", 0)
    return 0

def update_user_gold(uid: int, amount: int) -> int:
    user = users_collection.find_one({"uid": uid})
    if user:
        new_gold = user.get("gold", 0) + amount
        if new_gold < 0:
            new_gold = 0
        users_collection.update_one({"uid": uid}, {"$set": {"gold": new_gold}})
        return new_gold
    else:
        users_collection.insert_one({
            "uid": uid,
            "gold": max(0, amount),
            "inventory": [],
            "last_gift": 0,
            "banned": False
        })
        return max(0, amount)

# ======================
# دوال الهدايا اليومية
# ======================
def can_take_gift(uid: int) -> bool:
    user = users_collection.find_one({"uid": uid})
    if not user:
        return True
    last = user.get("last_gift", 0)
    return time.time() - last >= 86400

def take_gift(uid: int, amount: int = 100) -> int | None:
    if can_take_gift(uid):
        new_gold = update_user_gold(uid, amount)
        users_collection.update_one({"uid": uid}, {"$set": {"last_gift": time.time()}})
        return new_gold
    return None

# ======================
# دوال المخزون
# ======================
def get_inventory(uid: int) -> list:
    user = users_collection.find_one({"uid": uid})
    if user:
        return user.get("inventory", [])
    return []

def add_to_inventory(uid: int, item: str, quantity: int = 1) -> None:
    user = users_collection.find_one({"uid": uid})
    if user:
        inventory = user.get("inventory", [])
        inventory.extend([item] * quantity)
        users_collection.update_one({"uid": uid}, {"$set": {"inventory": inventory}})
    else:
        users_collection.insert_one({
            "uid": uid,
            "gold": 0,
            "inventory": [item] * quantity,
            "last_gift": 0,
            "banned": False
        })

def remove_from_inventory(uid: int, item: str, quantity: int = 1) -> bool:
    user = users_collection.find_one({"uid": uid})
    if not user:
        return False
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
# دوال الحظر والعفو
# ======================
def ban_user(uid: int) -> None:
    users_collection.update_one({"uid": uid}, {"$set": {"banned": True}}, upsert=True)

def unban_user(uid: int) -> None:
    users_collection.update_one({"uid": uid}, {"$set": {"banned": False}}, upsert=True)

def is_banned(uid: int) -> bool:
    user = users_collection.find_one({"uid": uid})
    if user:
        return user.get("banned", False)
    return False

def get_banned_users() -> list:
    return [u["uid"] for u in users_collection.find({"banned": True})]

# ======================
# دوال الحظر والعفو
# ======================

def ban_user(uid: int) -> None:
    users_collection.update_one(
        {"uid": uid},
        {"$set": {"banned": True}},
        upsert=True
    )

def unban_user(uid: int) -> None:
    users_collection.update_one(
        {"uid": uid},
        {"$set": {"banned": False}},
        upsert=True
    )

def is_user_banned(uid: int) -> bool:
    user = users_collection.find_one({"uid": uid})
    if not user:
        return False
    return user.get("banned", False)

def get_banned_users() -> list:
    banned = users_collection.find({"banned": True})
    return [user["uid"] for user in banned]
