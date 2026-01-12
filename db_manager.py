# ملف: db_manager.py
import motor.motor_asyncio
import time

# ======================
# إعداد MongoDB
# ======================
MONGO_URI = "mongodb+srv://wpee923_db_user:08520852KR@cluster0.nzjd5gc.mongodb.net/?retryWrites=true&w=majority"
DB_NAME = "imperial_bot"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
users_col = db["users"]
groups_col = db["groups"]

# ======================
# المطورين
# ======================
DEVELOPERS = [5860391324, 7076215547, 7855813063]

# ======================
# المستخدمين
# ======================
async def get_user(uid, name=None, username=None):
    user = await users_col.find_one({"uid": uid})
    if not user:
        user = {
            "uid": uid,
            "gold": 0,
            "bank": 0,
            "points": 0,
            "rank": 0,
            "last_gift_time": 0,
            "total_messages": 0,
            "level": 0,
            "name": name,
            "username": username,
            "married_to": None,
            "birthday": None,
            "birthday_auto": True
        }
        await users_col.insert_one(user)
    else:
        updates = {}
        if name and user.get("name") != name:
            updates["name"] = name
        if username and user.get("username") != username:
            updates["username"] = username
        if updates:
            await users_col.update_one({"uid": uid}, {"$set": updates})
    return await users_col.find_one({"uid": uid})

# ======================
# نقاط وفلوس
# ======================
async def get_user_gold(uid):
    user = await get_user(uid)
    return user.get("gold", 0)

async def update_user_gold(uid, amount):
    user = await get_user(uid)
    new_gold = max(0, user.get("gold", 0) + amount)
    await users_col.update_one({"uid": uid}, {"$set": {"gold": new_gold}})
    return new_gold

async def get_user_points(uid):
    user = await get_user(uid)
    return user.get("points", 0)

async def update_user_points(uid, amount):
    user = await get_user(uid)
    new_points = max(0, user.get("points", 0) + amount)
    await users_col.update_one({"uid": uid}, {"$set": {"points": new_points}})
    return new_points

# ======================
# البنك
# ======================
async def deposit_to_bank(uid, amount):
    user = await get_user(uid)
    if amount <= 0 or user.get("gold", 0) < amount:
        return False
    await users_col.update_one({"uid": uid}, {"$inc": {"gold": -amount, "bank": amount}})
    return True

async def withdraw_from_bank(uid, amount):
    user = await get_user(uid)
    if amount <= 0 or user.get("bank", 0) < amount:
        return False
    await users_col.update_one({"uid": uid}, {"$inc": {"bank": -amount, "gold": amount}})
    return True

# ======================
# الرتب
# ======================
async def get_user_rank(uid):
    user = await get_user(uid)
    return user.get("rank", 0)

async def set_user_rank(uid, rank):
    await users_col.update_one({"uid": uid}, {"$set": {"rank": rank}})

# ======================
# الهدايا اليومية
# ======================
DAY = 86400

async def can_take_gift(uid):
    user = await get_user(uid)
    return time.time() - user.get("last_gift_time", 0) >= DAY

async def take_gift(uid, amount=100):
    if not await can_take_gift(uid):
        return None
    await update_user_gold(uid, amount)
    await users_col.update_one({"uid": uid}, {"$set": {"last_gift_time": time.time()}})
    return await get_user_gold(uid)

# ======================
# الرسائل والمستوى
# ======================
async def get_user_message_count(uid):
    user = await get_user(uid)
    return user.get("total_messages", 0)

async def increment_user_message(uid):
    await users_col.update_one({"uid": uid}, {"$inc": {"total_messages": 1}}, upsert=True)

async def get_user_level(uid):
    user = await get_user(uid)
    return user.get("level", 0)

async def set_user_level(uid, level):
    await users_col.update_one({"uid": uid}, {"$set": {"level": level}}, upsert=True)

# ======================
# المجموعات: كتم وطرد
# ======================
async def mute_user(chat_id, user_id):
    group = await groups_col.find_one({"chat_id": chat_id})
    if not group:
        group = {"chat_id": chat_id, "muted": [], "kicked": []}
        await groups_col.insert_one(group)
    if user_id not in group["muted"]:
        group["muted"].append(user_id)
        await groups_col.update_one({"chat_id": chat_id}, {"$set": {"muted": group["muted"]}})

async def unmute_user(chat_id, user_id):
    group = await groups_col.find_one({"chat_id": chat_id})
    if group and user_id in group["muted"]:
        group["muted"].remove(user_id)
        await groups_col.update_one({"chat_id": chat_id}, {"$set": {"muted": group["muted"]}})

async def is_user_muted(chat_id, user_id):
    group = await groups_col.find_one({"chat_id": chat_id})
    return group and user_id in group.get("muted", [])

async def kick_user(chat_id, user_id):
    group = await groups_col.find_one({"chat_id": chat_id})
    if not group:
        group = {"chat_id": chat_id, "muted": [], "kicked": []}
        await groups_col.insert_one(group)
    if user_id not in group["kicked"]:
        group["kicked"].append(user_id)
        await groups_col.update_one({"chat_id": chat_id}, {"$set": {"kicked": group["kicked"]}})

async def get_muted_users(chat_id):
    group = await groups_col.find_one({"chat_id": chat_id})
    return group.get("muted", []) if group else []

async def get_kicked_users(chat_id):
    group = await groups_col.find_one({"chat_id": chat_id})
    return group.get("kicked", []) if group else []

# ======================
# التصدير
# ======================
__all__ = [
    "DEVELOPERS", "get_user", "get_user_gold", "update_user_gold", "get_user_points", "update_user_points",
    "get_user_rank", "set_user_rank",
    "can_take_gift", "take_gift",
    "get_user_message_count", "increment_user_message", "get_user_level", "set_user_level",
    "mute_user", "unmute_user", "is_user_muted", "kick_user",
    "get_muted_users", "get_kicked_users"
]
