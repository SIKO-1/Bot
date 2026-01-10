# ملف: cmd_marriage.py
import random
import time
from db_manager import _get_user, users

COMMANDS = ["زوجني", "طلقني", "قائمة المتزوجين"]

# ======================
# إعداد الزواج
# ======================
marriage_enabled = True

def is_already_married(uid):
    return users.find_one({"$or": [{"husband_uid": uid}, {"wife_uid": uid}]}) is not None

def get_marriage(uid):
    return users.find_one({"$or": [{"husband_uid": uid}, {"wife_uid": uid}]})

# ======================
# أمر زوجني
# ======================
def marry_user(bot, message, target_identifier):
    user = _get_user(message.from_user.id)
    
    if is_already_married(user["uid"]):
        bot.reply_to(message, "⚠️ أنت متزوج بالفعل!")
        return

    # البحث عن الشريك إما بالـ UID أو بالـ username
    target_user = None
    if target_identifier.startswith("@"):
        target_user = users.find_one({"username": target_identifier[1:]})
    else:
        try:
            target_uid = int(target_identifier)
            target_user = _get_user(target_uid)
        except:
            bot.reply_to(message, "⚠️ الرجاء كتابة رقم UID صالح أو @username")
            return

    if not target_user:
        bot.reply_to(message, "⚠️ لم يتم العثور على المستخدم المطلوب.")
        return

    if is_already_married(target_user["uid"]):
        bot.reply_to(message, "⚠️ هذا الشخص متزوج بالفعل!")
        return

    # تسجيل الزواج في MongoDB
    users.insert_one({
        "husband_uid": user["uid"],
        "wife_uid": target_user["uid"],
        "married_at": int(time.time())
    })

    bot.send_message(
        message.chat.id,
        f"💍 تم الزواج بنجاح بين:\n• {user['uid']} ({user.get('username', 'بدون اسم')})\n❤️\n• {target_user['uid']} ({target_user.get('username', 'بدون اسم')})"
    )

# ======================
# أمر طلقني
# ======================
def divorce(bot, message):
    user = _get_user(message.from_user.id)
    marriage = get_marriage(user["uid"])
    if not marriage:
        bot.reply_to(message, "⚠️ أنت غير متزوج حالياً!")
        return

    users.delete_one({"_id": marriage["_id"]})
    bot.reply_to(message, "💔 تم الطلاق بنجاح!")

# ======================
# قائمة المتزوجين
# ======================
def list_married(bot, message):
    all_marriages = list(users.find({"husband_uid": {"$exists": True}}))
    if not all_marriages:
        bot.reply_to(message, "لا يوجد متزوجين حالياً.")
        return

    text = "💑 قائمة المتزوجين:\n"
    for m in all_marriages:
        husband = _get_user(m["husband_uid"])
        wife = _get_user(m["wife_uid"])
        text += f"• {husband['uid']} ({husband.get('username', 'بدون اسم')}) ❤️ {wife['uid']} ({wife.get('username', 'بدون اسم')})\n"

    bot.send_message(message.chat.id, text)

# ======================
# Handler
# ======================
def handle(bot, message):
    if not marriage_enabled:
        return

    text = message.text.strip()
    uid = message.from_user.id

    if text.startswith("زوجني"):
        parts = text.split(maxsplit=1)
        if len(parts) < 2:
            bot.reply_to(message, "⚠️ الرجاء كتابة ID أو @username بعد 'زوجني'")
            return
        target_identifier = parts[1].strip()
        marry_user(bot, message, target_identifier)

    elif text == "طلقني":
        divorce(bot, message)

    elif text == "قائمة المتزوجين":
        list_married(bot, message)
