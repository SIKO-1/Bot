import random
from db_manager import get_user_gold, _get_user

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
# تحديد رتبة المستخدم في البوت
# ======================
def get_user_rank_in_bot(uid):
    user = _get_user(uid)
    rank_val = user.get("rank", 0)
    if rank_val == 0:
        return "عضو"
    elif rank_val == 1:
        return "مشرف"
    elif rank_val >= 2:
        return "مالك / مطور"
    else:
        return "عضو"

# ======================
# المعالج الرئيسي
# ======================
def handle(bot, message):
    DEV_ID = 5860391324
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
        # إذا المطور رد على رسالة شخص ثاني، نطلع ايدي هذا الشخص
        if message.reply_to_message and message.from_user.id == DEV_ID:
            user = message.reply_to_message.from_user
        else:
            user = message.from_user

        uid = user.id
        quote = random.choice(ID_QUOTES)
        gold = get_user_gold(uid)

        username = f"@{user.username}" if user.username else str(uid)
        bio = getattr(user, "bio", "") or ""  # ما يظهر "لا يوجد"
        rank = get_user_rank_in_bot(uid)

        account_type = "حساب مميز" if getattr(user, "is_premium", False) else "حساب عادي"

        text_id = f"""
↫ {quote}

⌁︙ايديڪ↫ {uid}
⌁︙معرفڪ↫ {username}
⌁︙حسابڪ↫ {account_type}
⌁︙رتبتڪ بالبـوت↫ {rank}
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
