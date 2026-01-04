import os
import time
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client['imperial_bot']
users_col = db['users']

def get_user_gold(uid):
    user = users_col.find_one({"_id": uid})
    return user.get("gold", 0) if user else 0

def update_user_gold(uid, amount):
    user = users_col.find_one({"_id": uid})
    if user:
        new_gold = max(0, user.get("gold", 0) + amount)
        users_col.update_one({"_id": uid}, {"$set": {"gold": new_gold}})
    else:
        users_col.insert_one({"_id": uid, "gold": max(0, amount), "items": [], "last_gift": 0})
        new_gold = max(0, amount)
    return new_gold

def can_take_gift(uid):
    user = users_col.find_one({"_id": uid})
    last = user.get("last_gift", 0) if user else 0
    return time.time() - last >= 86400

def take_gift(uid, amount=100):
    if can_take_gift(uid):
        users_col.update_one(
            {"_id": uid},
            {"$set": {"last_gift": time.time()}, "$inc": {"gold": amount}},
            upsert=True
        )
        return get_user_gold(uid)
    return None

def add_item(uid, item_name):
    users_col.update_one(
        {"_id": uid},
        {"$push": {"items": item_name}},
        upsert=True
    )

def get_items(uid):
    user = users_col.find_one({"_id": uid})
    return user.get("items", []) if user else []
