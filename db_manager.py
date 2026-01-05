import time
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# ======================
# إعداد MongoDB
# ======================
MONGO_URI = "mongodb+srv://wpee923_db_user:08520852KR@cluster0.nzjd5gc.mongodb.net/?retryWrites=true&w=majority"
DB_NAME = "imperial_bot"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
users = db["users"]

# ======================
# أدوات مساعدة
# ======================
def _get_user(uid: int):
    user = users.find_one({"uid": uid})
    if not user:
        user = {
            "uid": uid,
            "gold": 0,
            "bank": 0,
            "inventory": [],
            "last_gift": 0,
            "banned": False
        }
        users.insert_one(user)
    return user

# ======================
# الذهب (Gold)
# ======================
def get_user_gold(uid: int) -> int:
    return _get_user(uid).get("gold", 0)

def update_user_gold(uid: int, amount: int) -> int:
    user = _get_user(uid)
    new_gold = max(0, user["gold"] + amount)
    users.update_one({"uid": uid}, {"$set": {"gold": new_gold}})
    return new_gold

# ======================
# البنك (Bank)
# ======================
def get_user_bank(uid: int) -> int:
    return _get_user(uid).get("bank", 0)

def deposit_to_bank(uid: int, amount: int) -> bool:
    if amount <= 0:
        return False

    user = _get_user(uid)
    if user["gold"] < amount:
        return False

    users.update_one(
        {"uid": uid},
        {"$inc": {"gold": -amount, "bank": amount}}
    )
    return True

def withdraw_from_bank(uid: int, amount: int) -> bool:
    if amount <= 0:
        return False

    user = _get_user(uid)
    if user["bank"] < amount:
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
    users.update_one(
        {"uid": uid},
        {"$set": {"last_gift": time.time()}}
    )
    return get_user_gold(uid)

# ======================
# الحظر (Ban)
# ======================
def is_user_banned(uid: int) -> bool:
    return _get_user(uid).get("banned", False)

def ban_user(uid: int):
    users.update_one({"uid": uid}, {"$set": {"banned": True}})

def unban_user(uid: int):
    users.update_one({"uid": uid}, {"$set": {"banned": False}})
