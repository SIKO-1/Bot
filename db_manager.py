import pymongo

# الرابط السحابي الخاص بك
MONGO_URL = "mongodb+srv://wpee923_db_user:08520852KR@cluster0.nzjd5gc.mongodb.net/?appName=Cluster0"

try:
    client = pymongo.MongoClient(MONGO_URL)
    db = client["EmpireDB"]
    users_col = db["users"]
    commands_col = db["custom_commands"]
except Exception as e:
    print(f"❌ عطل في الاتصال السحابي: {e}")

def get_user(user_id):
    """جلب بيانات العضو من الذاكرة السحابية"""
    try:
        uid = str(user_id)
        user = users_col.find_one({"_id": uid})
        if not user:
            user = {"_id": uid, "gold": 0, "rank": "مواطن", "banned": False}
            users_col.insert_one(user)
        return user
    except:
        return None

def get_custom_command(name):
    """جلب الأوامر المخصصة (تم تصحيح الثغرة هنا)"""
    try:
        # البحث المباشر دون شروط مسبقة لمنع انهيار البوت
        cmd = commands_col.find_one({"_id": name})
        return cmd["reply"] if cmd else None
    except:
        return None
