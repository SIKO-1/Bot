import pymongo

# الرابط السحابي الخاص بك
MONGO_CONNECTION_STRING = "mongodb+srv://wpee923_db_user:08520852KR@cluster0.nzjd5gc.mongodb.net/?appName=Cluster0"

try:
    client = pymongo.MongoClient(MONGO_CONNECTION_STRING)
    db = client["EmpireDB"]
    users_collection = db["users"]
    commands_col = db["custom_commands"]
    print("✅ تم الاتصال بالحصن السحابي بنجاح.")
except Exception as e:
    print(f"❌ فشل الاتصال بالحصن السحابي: {e}")

def get_user(user_id):
    """جلب بيانات العضو من السحاب مباشرة"""
    try:
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
    except Exception as e:
        print(f"⚠️ خطأ في جلب بيانات العضو: {e}")
        return None

def update_user_gold(user_id, amount):
    """تعديل الذهب عبر تقنية الإضافة المباشرة"""
    try:
        uid = str(user_id)
        users_collection.update_one({"_id": uid}, {"$inc": {"gold": amount}}, upsert=True)
    except Exception as e:
        print(f"⚠️ خطأ في تحديث الذهب: {e}")

def get_user_gold(user_id):
    """الاستعلام عن رصيد الذهب"""
    user = get_user(user_id)
    return user.get("gold", 0) if user else 0

def increment_messages(user_id):
    """زيادة عداد المراسلات"""
    try:
        uid = str(user_id)
        users_collection.update_one({"_id": uid}, {"$inc": {"messages": 1}}, upsert=True)
    except Exception as e:
        print(f"⚠️ خطأ في عداد الرسائل: {e}")

# --- قسم الأوامر المخصصة (تصحيح خطأ NotImplementedError) ---

def save_custom_command(name, reply):
    """حفظ أمر جديد في الديوان السحابي"""
    try:
        commands_col.update_one(
            {"_id": name}, 
            {"$set": {"reply": reply}}, 
            upsert=True
        )
    except Exception as e:
        print(f"⚠️ خطأ في حفظ الأمر: {e}")

def get_custom_command(name):
    """جلب الرد المناسب من سجلات الإمبراطورية"""
    try:
        # تصحيح: تم حذف (if commands_col) لمنع انفجار البوت
        command = commands_col.find_one({"_id": name})
        return command["reply"] if command else None
    except Exception as e:
        print(f"⚠️ خطأ في استدعاء الأمر المخصص: {e}")
        return None

# --- إحصائيات الإمبراطورية ---

def get_total_users_count():
    return users_collection.count_documents({})

def get_total_messages():
    try:
        pipeline = [{"$group": {"_id": None, "total": {"$sum": "$messages"}}}]
        result = list(users_collection.aggregate(pipeline))
        return result[0]["total"] if result else 0
    except:
        return 0
