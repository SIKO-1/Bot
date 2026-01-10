# ملف: cmd_marriage.py
import time
from db_manager import _get_user, users, get_user_rank, set_user_rank

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
# أمر زوجني مع تحديد الشريك
# ======================
def marry_user(bot, message, target_identifier):
    user = _get_user(message.from_user.id)
    if is_already_married(user["uid"]):
        bot.reply_to(message, "⚠️ أنت متزوج بالفعل!")
        return

    # البحث عن الشريك بالـ ID أو username
    partner = None
    if target_identifier.startswith("@"):  # username
        username = target_identifier[1:]
        partner = users.find_one({"username": username})
    else:  # على افتراض أنه ID
        try:
            target_id = int(target_identifier)
            partner = users.find_one({"uid": target_id})
        except:
            bot.reply_to(message, "⚠️ الرجاء إدخال ID صالح أو اسم مستخدم صحيح.")
            return

    if not partner:
        bot.reply_to(message, "⚠️ هذا الشخص غير موجود.")
        return
    if is_already_married(partner["uid"]):
        bot.reply_to(message, "⚠️ هذا الشخص متزوج بالفعل!")
        return
    if partner["uid"] == user["uid"]:
        bot.reply_to(message, "⚠️ لا يمكنك الزواج بنفسك!")
        return

    # تسجيل الزواج
    users.insert_one({
        "husband_uid": user["uid"],
        "wife_uid": partner["uid"],
        "married_at": int(time.time())
    })

    bot.send_message(
        message.chat.id,
        f"💍 تم الزواج بنجاح!\n"
        f"👰 الزوج: {user.get('name','غير معروف')} (@{user.get('username','غير موجود')})\n"
        f"🤵 الزوجة: {partner.get('name','غير معروف')} (@{partner.get('username','غير موجود')})"
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
        husband = users.find_one({"uid": m["husband_uid"]})
        wife = users.find_one({"uid": m["wife_uid"]})
        text += f"• {husband.get('name','غير معروف')} (@{husband.get('username','غير موجود')}) ❤️ {wife.get('name','غير معروف')} (@{wife.get('username','غير موجود')})\n"

    bot.send_message(message.chat.id, text)

# ======================
# Handler
# ======================
def handle(bot, message):
    if not marriage_enabled:
        return

    text = message.text.strip()
    uid = message.from_user.id

    if text.startswith("زوجني "):
        target_identifier = text[6:].strip()
        marry_user(bot, message, target_identifier)
    elif text == "طلاقني":
        divorce(bot, message)
    elif text == "قائمة المتزوجين":
        list_married(bot, message)
