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

DAY = 86400  # 24 ساعة

# ======================
# المطورين
# ======================
DEVELOPERS = [
    5860391324,  # ID المطور
]

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
            "rank": 0,
            "last_task_time": 0,
            "daily_task": None,
            "box_ready": False,
            "box_opened": False,
            "last_gift_time": 0,
            "banned": False,
            "name": None,
            "username": None,
            "total_messages": 0,
            "married_to": None,
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
# المخزون
# ======================
def get_inventory(uid):
    return _get_user(uid).get("inventory", [])

def add_to_inventory(uid, item, quantity=1):
    user = _get_user(uid)
    inv = user.get("inventory", [])
    inv.extend([item] * quantity)
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
# الرتب
# ======================
def get_user_rank(uid):
    return _get_user(uid).get("rank", 0)

def set_user_rank(uid, rank):
    users.update_one({"uid": uid}, {"$set": {"rank": rank}})

def downgrade_user_rank(by_uid: int, target_uid: int, new_rank: int):
    if by_uid not in DEVELOPERS:
        return {"ok": False, "error": "❌ هذا الأمر للمطور فقط."}
    if new_rank < 0:
        new_rank = 0
    target = _get_user(target_uid)
    old_rank = target.get("rank", 0)
    if new_rank >= old_rank:
        return {"ok": False, "error": "⚠️ لا يمكن التخفيض لنفس الرتبة أو أعلى."}
    users.update_one({"uid": target_uid}, {"$set": {"rank": new_rank}})
    return {"ok": True, "old_rank": old_rank, "new_rank": new_rank}

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
    if user.get("daily_task"):
        return user["daily_task"]
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
    if not task or task["type"] != mission_type:
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

def can_take_gift(uid):
    user = _get_user(uid)
    return time.time() - user.get("last_gift_time", 0) >= DAY

# ======================
# الحظر
# ======================
def is_user_banned(uid):
    return _get_user(uid).get("banned", False)

def ban_user(uid):
    users.update_one({"uid": uid}, {"$set": {"banned": True}})

def unban_user(uid):
    users.update_one({"uid": uid}, {"$set": {"banned": False}})

# ======================
# إحصائيات
# ======================
def get_all_users_count():
    return users.count_documents({})

# ======================
# عيد الميلاد
# ======================
def add_birthday(uid: int, day: int, month: int, year: int = None):
    if day < 1 or day > 31 or month < 1 or month > 12:
        return {"ok": False, "error": "⚠️ التاريخ غير صالح."}
    users.update_one({"uid": uid}, {"$set": {"birthday": {"day": day, "month": month, "year": year}}})
    return {"ok": True, "uid": uid, "birthday": {"day": day, "month": month, "year": year}}

def remove_birthday(uid: int):
    users.update_one({"uid": uid}, {"$unset": {"birthday": ""}})
    return {"ok": True, "uid": uid}

def get_birthday(uid: int):
    user = _get_user(uid)
    return user.get("birthday", None)

def list_birthdays():
    result = []
    for user in users.find({"birthday": {"$exists": True}}):
        result.append({"uid": user["uid"], "birthday": user["birthday"]})
    return result

def enable_birthday_auto(uid: int):
    users.update_one({"uid": uid}, {"$set": {"birthday_auto": True}})
    return {"ok": True, "uid": uid}

def disable_birthday_auto(uid: int):
    users.update_one({"uid": uid}, {"$set": {"birthday_auto": False}})
    return {"ok": True, "uid": uid}

def is_birthday_auto_enabled(uid: int):
    user = _get_user(uid)
    return user.get("birthday_auto", False)

# ======================
# إعدادات المجموعات
# ======================
def set_photos_allowed(chat_id: int, allowed: bool):
    users.update_one(
        {"chat_id": chat_id},
        {"$set": {"photos_allowed": allowed}},
        upsert=True
    )

def set_stickers_allowed(chat_id: int, allowed: bool):
    users.update_one(
        {"chat_id": chat_id},
        {"$set": {"stickers_allowed": allowed}},
        upsert=True
    )

def is_photos_allowed(chat_id: int) -> bool:
    group = users.find_one({"chat_id": chat_id})
    if group and "photos_allowed" in group:
        return group["photos_allowed"]
    return True

def is_stickers_allowed(chat_id: int) -> bool:
    group = users.find_one({"chat_id": chat_id})
    if group and "stickers_allowed" in group:
        return group["stickers_allowed"]
    return True

# ======================
# إعدادات AI لكل مجموعة
# ======================
def set_ai_enabled(chat_id: int, enabled: bool):
    users.update_one(
        {"chat_id": chat_id},
        {"$set": {"ai_enabled": enabled}},
        upsert=True
    )

def get_ai_enabled(chat_id: int) -> bool:
    group = users.find_one({"chat_id": chat_id})
    if group and "ai_enabled" in group:
        return group["ai_enabled"]
    return True  # افتراضياً مفعل
