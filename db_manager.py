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
    users = db["users"]
    print("✅ MongoDB متصل بنجاح!")
except ConnectionFailure:
    print("❌ فشل الاتصال بـ MongoDB")

# ======================
# دوال مساعدة
# ======================
def _get_user(uid: int, username: str = None, first_name: str = None):
    """يرجع معلومات المستخدم ويحدث الاسم واليوزرنيم إذا تغيّر"""
    user = users.find_one({"uid": uid})
    if not user:
        user = {
            "uid": uid,
            "first_name": first_name or "غير معروف",
            "username": username or "لا يوجد",
            "gold": 0,
            "bank": 0,
            "inventory": [],
            "last_gift": 0,
            "banned": False,
            "total_messages": 0,
            "daily_usage": 0
        }
        users.insert_one(user)
    else:
        update = {}
        if username and user.get("username") != username:
            update["username"] = username
        if first_name and user.get("first_name") != first_name:
            update["first_name"] = first_name
        if update:
            users.update_one({"uid": uid}, {"$set": update})
    return user

# ======================
# الذهب
# ======================
def get_user_gold(uid: int) -> int:
    return _get_user(uid).get("gold", 0)

def update_user_gold(uid: int, amount: int) -> int:
    user = _get_user(uid)
    new_gold = max(0, user["gold"] + amount)
    users.update_one({"uid": uid}, {"$set": {"gold": new_gold}})
    return new_gold

# ======================
# البنك
# ======================
def get_user_bank(uid: int) -> int:
    return _get_user(uid).get("bank", 0)

def deposit_to_bank(uid: int, amount: int) -> bool:
    user = _get_user(uid)
    if amount <= 0 or user["gold"] < amount:
        return False
    users.update_one(
        {"uid": uid},
        {"$inc": {"gold": -amount, "bank": amount}}
    )
    return True

def withdraw_from_bank(uid: int, amount: int) -> bool:
    user = _get_user(uid)
    if amount <= 0 or user["bank"] < amount:
        return False
    users.update_one(
        {"uid": uid},
        {"$inc": {"bank": -amount, "gold": amount}}
    )
    return True

# ======================
# الهدايا اليومية
# ======================
def can_take_gift(uid: int) -> bool:
    user = _get_user(uid)
    return time.time() - user.get("last_gift", 0) >= 86400

def take_gift(uid: int, amount: int = 100):
    if not can_take_gift(uid):
        return None
    update_user_gold(uid, amount)
    users.update_one({"uid": uid}, {"$set": {"last_gift": time.time()}})
    return get_user_gold(uid)

# ======================
# الحظر والعفو
# ======================
def is_user_banned(uid: int) -> bool:
    return _get_user(uid).get("banned", False)

def ban_user(uid: int):
    users.update_one({"uid": uid}, {"$set": {"banned": True}})

def unban_user(uid: int):
    users.update_one({"uid": uid}, {"$set": {"banned": False}})

def list_banned_users() -> list:
    return [u["uid"] for u in users.find({"banned": True})]

# ======================
# المخزون / Inventory
# ======================
def get_inventory(uid: int) -> list:
    return _get_user(uid).get("inventory", [])

def add_to_inventory(uid: int, item: str, quantity: int = 1):
    user = _get_user(uid)
    inventory = user.get("inventory", [])
    inventory.extend([item] * quantity)
    users.update_one({"uid": uid}, {"$set": {"inventory": inventory}})

def remove_from_inventory(uid: int, item: str, quantity: int = 1) -> bool:
    user = _get_user(uid)
    inventory = user.get("inventory", [])
    count = 0
    new_inventory = []
    for i in inventory:
        if i == item and count < quantity:
            count += 1
            continue
        new_inventory.append(i)
    users.update_one({"uid": uid}, {"$set": {"inventory": new_inventory}})
    return count == quantity

# ======================
# إحصائيات المستخدمين
# ======================
def increment_messages(uid: int):
    users.update_one({"uid": uid}, {"$inc": {"total_messages": 1, "daily_usage": 1}})

def get_user_stats(uid: int) -> dict:
    user = _get_user(uid)
    return {
        "first_name": user.get("first_name", "غير معروف"),
        "username": user.get("username", "لا يوجد"),
        "gold": user.get("gold", 0),
        "bank": user.get("bank", 0),
        "inventory": user.get("inventory", []),
        "total_messages": user.get("total_messages", 0),
        "daily_usage": user.get("daily_usage", 0),
        "banned": user.get("banned", False)
    }

def get_all_users_count() -> int:
    return users.count_documents({})

def reset_daily_usage():
    users.update_many({}, {"$set": {"daily_usage": 0}})

# ======================
# مهمات يومية وصناديق الحظ
# ======================
def set_daily_task(uid, task):
    users.update_one({"uid": uid}, {"$set": {"daily_task": task, "box_ready": False, "box_opened": False}})

def get_daily_task(uid):
    return _get_user(uid).get("daily_task", "")

def complete_daily_task(uid):
    users.update_one({"uid": uid}, {"$set": {"box_ready": True, "daily_task": ""}})

def can_open_box(uid):
    user = _get_user(uid)
    return user.get("box_ready", False) and not user.get("box_opened", False)

def set_box_opened(uid):
    users.update_one({"uid": uid}, {"$set": {"box_opened": True}})
