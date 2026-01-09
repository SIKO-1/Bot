# ملف: cmd_marriage.py
import random
from db_manager import _get_user, get_user_rank, set_user_rank, users
import time

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
# توليد ميمز للزوجين
# ======================
def generate_meme(husband_user, wife_user):
    # مجرد نص ميمز، يمكن تغييره لأي صورة في المستقبل
    return f"💞 {husband_user['uid']} ❤️ {wife_user['uid']} - مبروك الزواج!"

# ======================
# أمر زوجني
# ======================
def marry_random(bot, message):
    user = _get_user(message.from_user.id)
    if is_already_married(user["uid"]):
        bot.reply_to(message, "⚠️ أنت متزوج بالفعل!")
        return

    # جلب جميع المستخدمين غير المتزوجين عشوائياً
    all_users = list(users.find({"uid": {"$ne": user["uid"]}}))
    candidates = [u for u in all_users if not is_already_married(u["uid"])]
    if not candidates:
        bot.reply_to(message, "⚠️ لا يوجد أحد متاح للزواج حالياً.")
        return

    partner = random.choice(candidates)

    # تسجيل الزواج في MongoDB
    users.insert_one({
        "husband_uid": user["uid"],
        "wife_uid": partner["uid"],
        "married_at": int(time.time())
    })

    meme = generate_meme(user, partner)
    bot.send_message(message.chat.id, f"💍 تم الزواج بنجاح بين {user['uid']} ❤️ {partner['uid']}")
    bot.send_message(message.chat.id, meme)

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
        text += f"• {m['husband_uid']} ❤️ {m['wife_uid']}\n"
    bot.send_message(message.chat.id, text)

# ======================
# Handler
# ======================
def handle(bot, message):
    if not marriage_enabled:
        return

    text = message.text.strip()
    uid = message.from_user.id

    if text == "زوجني":
        marry_random(bot, message)
    elif text == "طلقني":
        divorce(bot, message)
    elif text == "قائمة المتزوجين":
        list_married(bot, message)
