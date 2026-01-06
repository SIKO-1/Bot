import time
import random
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

DAY = 86400  # 24 ساعة بالثواني

# ======================
# جلب / إنشاء مستخدم
# ======================
def _get_user(uid: int):
    user = users.find_one({"uid": uid})
    if not user:
        user = {
            "uid": uid,
            "gold": 0,
            "bank": 0,
            "inventory": [],
            "last_task_time": 0,
            "daily_task": None,
            "box_ready": False,
            "box_opened": False,
        }
        users.insert_one(user)
    return users.find_one({"uid": uid})

# ======================
# الذهب
# ======================
def get_user_gold(uid):
    return _get_user(uid)["gold"]

def update_user_gold(uid, amount):
    user = _get_user(uid)
    new_gold = max(0, user["gold"] + amount)
    users.update_one({"uid": uid}, {"$set": {"gold": new_gold}})
    return new_gold

# ======================
# البنك
# ======================
def get_user_bank(uid):
    return _get_user(uid)["bank"]

def deposit_to_bank(uid, amount):
    user = _get_user(uid)
    if amount <= 0 or user["gold"] < amount:
        return False
    users.update_one({"uid": uid}, {"$inc": {"gold": -amount, "bank": amount}})
    return True

def withdraw_from_bank(uid, amount):
    user = _get_user(uid)
    if amount <= 0 or user["bank"] < amount:
        return False
    users.update_one({"uid": uid}, {"$inc": {"bank": -amount, "gold": amount}})
    return True

# ======================
# المخزون / Inventory
# ======================
def get_inventory(uid):
    return _get_user(uid).get("inventory", [])

def add_to_inventory(uid, item, quantity=1):
    user = _get_user(uid)
    inv = user.get("inventory", [])
    inv.extend([item]*quantity)
    users.update_one({"uid": uid}, {"$set": {"inventory": inv}})

def remove_from_inventory(uid, item, quantity=1):
    user = _get_user(uid)
    inv = user.get("inventory", [])
    count = 0
    new_inv = []
    for i in inv:
        if i == item and count < quantity:
            count += 1
            continue
        new_inv.append(i)
    users.update_one({"uid": uid}, {"$set": {"inventory": new_inv}})
    return count == quantity

# ======================
# المهام اليومية
# ======================
TASKS = [
    {"type": "dice", "desc": "العب لعبة النرد 🎲"},
    {"type": "roulette", "desc": "العب روليت 🎰"},
]

def can_get_task(uid):
    user = _get_user(uid)
    return time.time() - user.get("last_task_time", 0) >= DAY

def time_left_for_task(uid):
    user = _get_user(uid)
    remaining = DAY - (time.time() - user.get("last_task_time", 0))
    if remaining <= 0:
        return None
    hours = int(remaining // 3600)
    minutes = int((remaining % 3600) // 60)
    return f"{hours} ساعة و {minutes} دقيقة"

def get_daily_task(uid):
    user = _get_user(uid)
    # لو عنده مهمة حالياً
    if user.get("daily_task"):
        return user["daily_task"]
    # لو ما يقدر ياخذ مهمة جديدة
    if not can_get_task(uid):
        return None
    task = random.choice(TASKS)
    users.update_one(
        {"uid": uid},
        {"$set": {
            "daily_task": task,
            "last_task_time": time.time(),
            "box_ready": False,
            "box_opened": False
        }}
    )
    return task

def complete_mission(uid, mission_type):
    user = _get_user(uid)
    task = user.get("daily_task")
    if not task:
        return False
    if task["type"] != mission_type:
        return False
    users.update_one({"uid": uid}, {"$set": {"box_ready": True, "daily_task": None}})
    return True

def can_open_box(uid):
    user = _get_user(uid)
    return user.get("box_ready", False) and not user.get("box_opened", False)

def set_box_opened(uid):
    users.update_one({"uid": uid}, {"$set": {"box_opened": True}})

# ======================
# الهدايا اليومية
# ======================
def take_gift(uid, amount=100):
    user = _get_user(uid)
    last = user.get("last_gift_time", 0)
    if time.time() - last < DAY:
        return None
    update_user_gold(uid, amount)
    users.update_one({"uid": uid}, {"$set": {"last_gift_time": time.time()}})
    return get_user_gold(uid)

# ======================
# إحصائيات المستخدمين
# ======================
def get_all_users_count():
    return users.count_documents({})
