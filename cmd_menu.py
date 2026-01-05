import random
from db_manager import get_user_gold

# ======================
# جمل عشوائية للهوية
# ======================
ID_QUOTES = [
    "مو كل اسم ينكتب… بعضهم ينحفر.",
    "الحضور ما يحتاج تعريف.",
    "الهيبة أسلوب، مو ضجيج.",
    "مكانك ثابت حتى لو تغيّر المكان.",
    "الصمت أحيانًا أفخم من الكلام.",
    "مو رقم… هو توقيع.",
    "الاسم بسيط، التأثير ثقيل.",
    "الهيبة ما تنشرح، تنفهم.",
    "مو نسخة، أصل.",
    "بعض الناس ما يحتاجون لقب."
]

# ======================
# قائمة الأوامر
# ======================
MENU_TEXT = """
╔═════════════════╗
   الأوامر الإمبراطورية
╚═════════════════╝

مرحباً بك في بوت كيرا
يا {name}

━━━━━━━━━━━━━━━

الأقسام :

• الألعاب
• المتجر
• البنك
• تسلية 
• شؤون الإدارة

━━━━━━━━━━━━━━━

شؤون الإدارة :
• إدارة

━━━━━━━━━━━━━━━
لعرض هويتك أرسل :
〔 ا 〕 أو 〔 ايدي 〕

━━━━━━━━━━━━━━━
الدنيا مو عادلة… بس الهيبة تختار أصحابها.
"""

# ======================
# تحديد رتبة المستخدم
# ======================
def get_user_rank(bot, chat_id, user_id):
    try:
        member = bot.get_chat_member(chat_id, user_id)
        if member.status == "creator":
            return "مالك المجموعة"
        elif member.status == "administrator":
            return "مشرف"
        else:
            return "عضو"
    except:
        return "غير معروف"

# ======================
# المعالج الرئيسي
# ======================
def handle(bot, message):
    text = message.text.strip()

    # ===== قائمة الأوامر =====
    if text in ["اوامر", "الأوامر"]:
        bot.reply_to(
            message,
            MENU_TEXT.format(name=message.from_user.first_name)
        )
        return

    # ===== أمر الايدي =====
    if text in ["ا", "ايدي"]:
        user = message.from_user
        uid = user.id

        quote = random.choice(ID_QUOTES)
        gold = get_user_gold(uid)

        username = f"@{user.username}" if user.username else "—"
        bio = user.bio if hasattr(user, "bio") and user.bio else "لا يوجد"
        rank = get_user_rank(bot, message.chat.id, uid)

        account_type = "حساب مميز" if user.is_premium else "حساب عادي"

        text_id = f"""
↫ {quote}

⌁︙ايديڪ↫ {uid}
⌁︙معرفڪ↫ {username}
⌁︙حسابڪ↫ {account_type}
⌁︙رتبتڪ↫ {rank}
⌁︙فلوسڪ↫ {gold} ذهب
⌁︙البـايـــو↫ {bio}
"""

        # صورة الحساب إن وجدت
        try:
            photos = bot.get_user_profile_photos(uid, limit=1)
            if photos.total_count > 0:
                bot.send_photo(
                    message.chat.id,
                    photos.photos[0][-1].file_id,
                    caption=text_id
                )
            else:
                bot.reply_to(message, text_id)
        except:
            bot.reply_to(message, text_id)
