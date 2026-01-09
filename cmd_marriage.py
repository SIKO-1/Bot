import telebot
import random
from db_manager import _get_user, users
import time

COMMANDS = ["زوجني", "زوجني@", "طلقني", "قائمة المتزوجين"]

# رابط صورة الميمز الثابتة
MEME_IMAGE_URL = "https://www2.0zz0.com/2026/01/09/22/600117073.jpg"


# ======================
# المساعدات
# ======================
def is_already_married(uid):
    return users.count_documents({
        "$or": [
            {"husband_uid": uid},
            {"wife_uid": uid}
        ]
    }) > 0

def get_marriage(uid):
    return users.find_one({
        "$or": [
            {"husband_uid": uid},
            {"wife_uid": uid}
        ]
    })


# ======================
# الزواج العشوائي أو المحدد
# ======================
def do_marry(bot, message, target_uid=None):

    user_uid = message.from_user.id
    if is_already_married(user_uid):
        bot.reply_to(message, "⚠️ انت متزوج حالياً!")
        return

    # -------- زواج محدد بالرد أو بالايدي --------
    if target_uid:
        # حذف <@> إذا مستخدم
        try:
            target_uid = int(target_uid)
        except:
            bot.reply_to(message, "❌ الايدي غير صالح!")
            return
        if target_uid == user_uid:
            bot.reply_to(message, "⚠️ ما تگدر تتزوج نفسك 😉")
            return
        if is_already_married(target_uid):
            bot.reply_to(message, "⚠️ الشخص هذا متزوج بالفعل!")
            return
        partner = _get_user(target_uid)
    else:
        # -------- زواج عشوائي من المستخدمين --------
        all_users = list(users.find({"uid": {"$ne": user_uid}}))
        # فلترة غير المتزوجين
        candidates = [u for u in all_users if not is_already_married(u["uid"])]
        if not candidates:
            bot.reply_to(message, "⚠️ لا يوجد أحد متاح للزواج حالياً!")
            return
        partner = random.choice(candidates)

    # تسجيل الزواج في DB
    marriage_data = {
        "husband_uid": user_uid,
        "wife_uid": partner["uid"],
        "married_at": int(time.time())
    }
    users.insert_one(marriage_data)

    # تجهيز صور الحسابات
    try:
        # صورة الزوج
        husband_photo = None
        photos = bot.get_user_profile_photos(user_uid, limit=1)
        if photos.total_count > 0:
            husband_photo = photos.photos[0][-1].file_id

        # صورة الزوجة
        wife_photo = None
        photos2 = bot.get_user_profile_photos(partner["uid"], limit=1)
        if photos2.total_count > 0:
            wife_photo = photos2.photos[0][-1].file_id

    except:
        husband_photo = None
        wife_photo = None

    # إرسال صورة الميمز + صور المتزوجين
    caption = f"💍 تم الزواج بنجاح!\n🤵🏻 الزوج: {user_uid}\n👰🏻‍♀️ الزوجة: {partner['uid']}"

    # إذا كل الصور المتوفرة
    try:
        # نبعث أولاً صورة الميمز
        bot.send_photo(message.chat.id, MEME_IMAGE_URL, caption=caption)

        # نبعث صورة الزوج
        if husband_photo:
            bot.send_photo(message.chat.id, husband_photo, caption="📸 صورة الزوج")
        # نبعث صورة الزوجة
        if wife_photo:
            bot.send_photo(message.chat.id, wife_photo, caption="📸 صورة الزوجة")

    except Exception as e:
        bot.reply_to(message, f"⚠️ صار خطأ بإرسال الصور: {e}")


# ======================
# الأمر طلاق
# ======================
def do_divorce(bot, message):
    user_uid = message.from_user.id
    marriage = get_marriage(user_uid)
    if not marriage:
        bot.reply_to(message, "⚠️ انت مو متزوج!")
        return
    users.delete_one({"_id": marriage["_id"]})
    bot.reply_to(message, "💔 تم الطلاق بنجاح!")


# ======================
# قائمة المتزوجين
# ======================
def show_list(bot, message):
    all_marriages = list(users.find({"husband_uid": {"$exists": True}}))
    if not all_marriages:
        bot.reply_to(message, "⚠️ لا يوجد متزوجين حالياً!")
        return

    text = "💑 قائمة المتزوجين:\n"
    for m in all_marriages:
        text += f"• {m['husband_uid']} ❤️ {m['wife_uid']}\n"
    bot.send_message(message.chat.id, text)


# ======================
# معالجة الـCMD
# ======================
def handle(bot, message):
    text = message.text.strip()

    if text.startswith("زوجني"):
        # إذا مكتوب "زوجني" بدون شي، نزوجك عشوائي
        do_marry(bot, message)

    elif text.startswith("زوجني "):
        # زواج محدد بالايدي
        parts = text.split()
        if len(parts) >= 2:
            do_marry(bot, message, parts[1])

    elif text == "طلقني":
        do_divorce(bot, message)

    elif text == "قائمة المتزوجين":
        show_list(bot, message)
