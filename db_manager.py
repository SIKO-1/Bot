from pymongo import MongoClient

# ⚠️ ضع كلمة سرك مكان النص العربي أدناه ولا تمسح النقطتين : أو علامة @
MONGO_URL = "mongodb+srv://wpee923_db_user:08520852KR@cluster0.nzjd5gc.mongodb.net/?appName=Cluster0"

client = MongoClient(MONGO_URL)
db = client['EmpireDB']
users_col = db['users']

def get_user(user_id):
    uid = str(user_id)
    user = users_col.find_one({"user_id": uid})
    if not user:
        new_user = {"user_id": uid, "balance": 0, "inventory": [], "rank": "مبتدئ", "bio": "لا يوجد"}
        users_col.insert_one(new_user)
        return new_user
    return user

def update_user(user_id, key, value):
    uid = str(user_id)
    users_col.update_one({"user_id": uid}, {"$set": {key: value}})

def get_balance(user_id):
    return get_user(user_id).get('balance', 0)

def update_balance(user_id, amount):
    uid = str(user_id)
    users_col.update_one({"user_id": uid}, {"$inc": {"balance": amount}})
