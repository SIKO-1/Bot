import pymongo

# الرابط السحابي الخاص بك (تم الحفاظ عليه كما هو)
MONGO_CONNECTION_STRING = "mongodb+srv://wpee923_db_user:08520852KR@cluster0.nzjd5gc.mongodb.net/?appName=Cluster0"

try:
    client = pymongo.MongoClient(MONGO_CONNECTION_STRING)
    db = client["EmpireDB"]
    users_collection = db["users"]
    commands_col = db["custom_commands"]
    # إضافة مجموعة خاصة للمجموعات (الأقاليم) لدعم نظام الخصم
    groups_col = db["groups"] 
except Exception as e:
    print(f"فشل الاتصال بالحصن السحابي: {e}")

# --- إدارة شؤون الرعية والمستويات ---

def get_user(user_id):
    """جلب بيانات العضو من السحاب مع دعم المستويات"""
    uid = str(user_id)
    user = users_collection.find_one({"_id": uid})
    if not user:
        user = {
            "_id": uid, 
            "gold": 0, 
            "messages": 0, 
            "xp": 0,  # نظام الخبرة الجديد
            "rank": "مواطن", 
            "banned": False,
            "last_gift": None
        }
        users_collection.insert_one(user)
    return user

def update_user_experience(user_id, xp_amount):
    """زيادة وقار (خبرة) العضو في السحاب"""
    try:
        uid = str(user_id)
        users_collection.update_one(
            {"_id": uid}, 
            {"$inc": {"xp": xp_amount}}, 
            upsert=True
        )
    except Exception as e:
        print(f"⚠️ تنبيه إمبراطوري: فشل تحديث الخبرة: {e}")

def get_user_level(user_id):
    """حساب المستوى بناءً على الخبرة السحابية"""
    try:
        user = get_user(user_id)
        xp = user.get("xp", 0)
        # كل 500 نقطة خبرة ترفع العضو مستوى واحد
        level = int(xp / 500)
        return level, xp
    except:
        return 0, 0

# --- إدارة الأموال (الذهب) ---

def get_user_gold(user_id):
    return get_user(user_id).get("gold", 0)

def update_user_gold(user_id, amount):
    uid = str(user_id)
    users_collection.update_one({"_id": uid}, {"$inc": {"gold": amount}}, upsert=True)

# --- إدارة الأقاليم (المجموعات) ---

def add_group(chat_id):
    """تسجيل المجموعة لتصلها نداءات الحرب (الخصم)"""
    cid = str(chat_id)
    groups_col.update_one({"_id": cid}, {"$set": {"active": True}}, upsert=True)

def get_all_active_chats():
    """جلب قائمة المجموعات النشطة"""
    return [int(g["_id"]) for g in groups_col.find({"active": True})]

# --- الأوامر المخصصة (المراسيم) ---

def save_custom_command(name, reply):
    commands_col.update_one({"_id": name}, {"$set": {"reply": reply}}, upsert=True)

def get_custom_command(name):
    command = commands_col.find_one({"_id": name})
    return command["reply"] if command else None
