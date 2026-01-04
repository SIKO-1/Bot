import pymongo

# هذا هو الرابط السحابي الخاص بك
# قم بوضع كلمة المرور مكان كلمة PASSWORD_HERE
MONGO_CONNECTION_STRING = "mongodb+srv://wpee923_db_user:08520852KR@cluster0.nzjd5gc.mongodb.net/?appName=Cluster0"

try:
    client = pymongo.MongoClient(MONGO_CONNECTION_STRING)
    db = client["EmpireDB"]
    users_collection = db["users"]
except Exception as e:
    print(f"فشل الاتصال بالحصن السحابي: {e}")

def get_user(user_id):
    """جلب بيانات العضو من السحاب مباشرة"""
    uid = str(user_id)
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
        users_collection.insert_one(user)
    return user

def update_user(user_id, data):
    """تحديث بيانات العضو في السحاب"""
    uid = str(user_id)
    users_collection.update_one({"_id": uid}, {"$set": data}, upsert=True)

def get_user_gold(user_id):
    """الاستعلام عن رصيد الذهب"""
    user = get_user(user_id)
    return user.get("gold", 0)

def update_user_gold(user_id, amount):
    """تعديل الذهب عبر تقنية الإضافة المباشرة لمنع التصفير"""
    uid = str(user_id)
    users_collection.update_one({"_id": uid}, {"$inc": {"gold": amount}}, upsert=True)

def increment_messages(user_id):
    """زيادة عداد المراسلات"""
    uid = str(user_id)
    users_collection.update_one({"_id": uid}, {"$inc": {"messages": 1}}, upsert=True)

# --- إحصائيات الإمبراطورية ---

def get_total_users_count():
    """تعداد الرعية في المملكة"""
    return users_collection.count_documents({})

def get_banned_users_count():
    """تعداد المنفيين من الديار"""
    return users_collection.count_documents({"banned": True})

def get_total_messages():
    """مجموع مراسلات الرعية"""
    pipeline = [{"$group": {"_id": None, "total": {"$sum": "$messages"}}}]
    result = list(users_collection.aggregate(pipeline))
    return result[0]["total"] if result else 0

# --- قسم الأوامر المخصصة (السحابي) ---

def save_custom_command(name, reply):
    """حفظ أمر جديد في الديوان السحابي"""
    # نستخدم مجموعة (Collection) خاصة للأوامر المخصصة
    commands_col = db["custom_commands"]
    commands_col.update_one(
        {"_id": name}, 
        {"$set": {"reply": reply}}, 
        upsert=True
    )

def get_custom_command(name):
    """جلب الرد المناسب من سجلات الإمبراطورية"""
    commands_col = db["custom_commands"]
    command = commands_col.find_one({"_id": name})
    return command["reply"] if command else None
