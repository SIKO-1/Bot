# ملف: cmd_ban_db.py
import telebot
import time
from pymongo import MongoClient
from datetime import datetime

DEVELOPER_ID = 5860391324

# ======================
# إعداد MongoDB
# ======================
MONGO_URI = "mongodb+srv://wpee923_db_user:08520852KR@cluster0.nzjd5gc.mongodb.net/?retryWrites=true&w=majority"
DB_NAME = "imperial_bot"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
bans_collection = db["bans"]

COMMANDS = ["حظر", "عفو", "قائمة_المحظورين"]

def is_banned(uid: int) -> bool:
    return bans_collection.find_one({"uid": uid}) is not None

def add_ban(uid: int, name: str):
    if not is_banned(uid):
        bans_collection.insert_one({
            "uid": uid,
            "name": name,
            "time": time.time()
        })

def remove_ban(uid: int):
    bans_collection.delete_one({"uid": uid})

def handle(bot, message):
    uid = message.from_user.id

    # 1️⃣ التحقق من المحظورين
    if is_banned(uid) and uid != DEVELOPER_ID:
        bot.reply_to(message, "اُصمت! جاء أمر من الإمبراطور بنفيك خارج مملكته! 👑")
        return

    # 2️⃣ الأوامر الخاصة بالمطور فقط
    if uid != DEVELOPER_ID:
        return

    text = message.text.split()
    cmd = text[0]

    # ===== حظر شخص بالرد =====
    if cmd == "حظر":
        if not message.reply_to_message:
            bot.reply_to(message, "❌ يجب الرد على رسالة الشخص الذي تريد حظره!")
            return
        target_user = message.reply_to_message.from_user
        add_ban(target_user.id, target_user.first_name)
        bot.reply_to(message, f"✅ تم حظر المستخدم {target_user.first_name} من مملكة البوت 👑")
        return

    # ===== عفو عن شخص بالرد =====
    if cmd == "عفو":
        if not message.reply_to_message:
            bot.reply_to(message, "❌ يجب الرد على رسالة الشخص الذي تريد العفو عنه!")
            return
        target_user = message.reply_to_message.from_user
        if is_banned(target_user.id):
            remove_ban(target_user.id)
            bot.reply_to(message, f"✅ تم العفو عن المستخدم {target_user.first_name} 👑")
            bot.send_message(target_user.id, "بأمر من الإمبراطور تم العفو عنك، اشكره! 👑")
        else:
            bot.reply_to(message, "⚠️ هذا الشخص ليس محظوراً بالفعل!")
        return

    # ===== عرض قائمة المحظورين =====
    if cmd == "قائمة_المحظورين":
        banned_users = bans_collection.find()
        banned_list = list(banned_users)
        if not banned_list:
            bot.reply_to(message, "📜 لا يوجد مستخدمين محظورين حالياً.")
            return

        text_list = "📜 قائمة المحظورين الحاليين:\n"
        for u in banned_list:
            ban_time = datetime.fromtimestamp(u["time"]).strftime("%Y-%m-%d %H:%M:%S")
            text_list += f"• {u['name']} (ID: {u['uid']}) → تم الحظر في: {ban_time}\n"
        bot.reply_to(message, text_list)
