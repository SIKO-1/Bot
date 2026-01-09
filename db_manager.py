import time
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
    users = db["users"]          # قاعدة المستخدمين الأساسية
    marriages = db["marriages"]  # جدول حفظ بيانات الزواج
    print("✅ MongoDB متصل بنجاح!")
except ConnectionFailure:
    print("❌ فشل الاتصال بـ MongoDB")

# ======================
# الزواج
# ======================
def get_marriage(uid):
    """جلب بيانات الزواج لشخص"""
    return marriages.find_one({"uid": uid})

def is_married(uid):
    """هل الشخص متزوج؟"""
    return marriages.count_documents({"uid": uid}) > 0

def marry(uid1, uid2, timestamp=None):
    """
    زواج شخصين
    uid1: الشخص الأول
    uid2: الشخص الثاني
    timestamp: وقت الزواج (unix)
    """
    if is_married(uid1) or is_married(uid2):
        return {"ok": False, "error": "⚠️ واحد من الطرفين متزوج بالفعل."}

    if timestamp is None:
        timestamp = int(time.time())

    marriage_data = {
        "uid": uid1,
        "spouse_uid": uid2,
        "timestamp": timestamp
    }
    marriages.insert_one(marriage_data)

    # نسوي البيانات للطرف الثاني عشان يظهر متزوج كمان
    marriage_data_2 = {
        "uid": uid2,
        "spouse_uid": uid1,
        "timestamp": timestamp
    }
    marriages.insert_one(marriage_data_2)

    return {"ok": True, "uid1": uid1, "uid2": uid2, "timestamp": timestamp}

def divorce(uid):
    """فك الزواج عن شخص"""
    marriage = get_marriage(uid)
    if not marriage:
        return {"ok": False, "error": "⚠️ هذا الشخص غير متزوج."}

    spouse_uid = marriage["spouse_uid"]
    marriages.delete_many({"uid": uid})
    marriages.delete_many({"uid": spouse_uid})

    return {"ok": True, "uid": uid, "ex_spouse": spouse_uid}

def list_all_marriages():
    """جلب قائمة كل المتزوجين"""
    result = []
    seen = set()
    for m in marriages.find():
        uid1 = m["uid"]
        uid2 = m["spouse_uid"]
        # نتجنب التكرار
        key = tuple(sorted([uid1, uid2]))
        if key not in seen:
            result.append({"uid1": uid1, "uid2": uid2, "timestamp": m["timestamp"]})
            seen.add(key)
    return result

# ======================
# زواج عشوائي
# ======================
def marry_random(uid, eligible_uids):
    """
    تزويج شخص مع شخص عشوائي من القائمة eligible_uids
    """
    import random
    available = [u for u in eligible_uids if not is_married(u) and u != uid]
    if not available:
        return {"ok": False, "error": "⚠️ لا يوجد أشخاص متاحين للزواج."}

    spouse_uid = random.choice(available)
    return marry(uid, spouse_uid)
