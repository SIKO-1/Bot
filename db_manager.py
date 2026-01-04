import pymongo

# الرابط السحابي
MONGO_CONNECTION_STRING = "mongodb+srv://wpee923_db_user:08520852KR@cluster0.nzjd5gc.mongodb.net/?appName=Cluster0"

# --- إنشاء اتصال MongoDB بطريقة آمنة ---
try:
    client = pymongo.MongoClient(
        MONGO_CONNECTION_STRING,
        serverSelectionTimeoutMS=5000,  # 5 ثواني انتظار للاتصال
        connect=True
    )
    db = client["EmpireDB"]
    users_collection = db["users"]
    commands_col = db["custom_commands"]
    # تحقق من الاتصال
    client.admin.command("ping")
except Exception as e:
    print(f"❌ فشل الاتصال بالحصن السحابي: {e}")
    users_collection = None
    commands_col = None

# --- المستخدمين ---
def get_user(user_id):
    uid = str(user_id)
    if users_collection is None:
        return None
    user = users_collection.find_one({"_id": uid})
    if not user:
        user = {
            "_id": uid, 
            "gold": 0, 
            "messages": 0, 
            "rank": "مواطن", 
            "banned": False,
            "last_gift": None
        }
        users_collection.update_one({"_id": uid}, {"$setOnInsert": user}, upsert=True)
    return user

def update_user(user_id, data):
    uid = str(user_id)
    if users_collection is None:
        return
    users_collection.update_one({"_id": uid}, {"$set": data}, upsert=True)

def get_user_gold(user_id):
    user = get_user(user_id)
    return user.get("gold", 0) if user else 0

def update_user_gold(user_id, amount):
    if not isinstance(amount, int):
        amount = 0
    uid = str(user_id)
    if users_collection:
        users_collection.update_one({"_id": uid}, {"$inc": {"gold": amount}}, upsert=True)

def increment_messages(user_id):
    uid = str(user_id)
    if users_collection:
        users_collection.update_one({"_id": uid}, {"$inc": {"messages": 1}}, upsert=True)

# --- إحصائيات ---
def get_total_users_count():
    return users_collection.count_documents({}) if users_collection else 0

def get_banned_users_count():
    return users_collection.count_documents({"banned": True}) if users_collection else 0

def get_total_messages():
    if not users_collection:
        return 0
    pipeline = [{"$group": {"_id": None, "total": {"$sum": "$messages"}}}]
    result = list(users_collection.aggregate(pipeline))
    return result[0]["total"] if result else 0

# --- أوامر مخصصة ---
def save_custom_command(name, reply):
    if commands_col:
        commands_col.update_one({"_id": name}, {"$set": {"reply": reply}}, upsert=True)

def get_custom_command(name):
    if commands_col:
        command = commands_col.find_one({"_id": name})
        return command.get("reply") if command else None
    return None
