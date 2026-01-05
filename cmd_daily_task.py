import db_manager
from telebot.types import Message
import random

COMMANDS = ["مهمتي", "فتح الصندوق"]

# جوائز عشوائية للصندوق
BOX_REWARDS = ["ذهب:500", "ذهب:1000", "جوهرة نادرة", "صندوق إضافي", "ذهب:200"]

# عدد الرسائل المطلوبة كمثال لإكمال المهمة
DAILY_MESSAGE_TARGET = 40

def handle(bot, message: Message):
    uid = message.from_user.id
    first_name = message.from_user.first_name
    username = message.from_user.username

    text = message.text.strip()

    # ======================
    # إعطاء المهمة اليومية تلقائيًا
    # ======================
    if text.lower() == "مهمتي":
        task = db_manager.get_daily_task(uid)
        if not task:
            # توليد مهمة عشوائية
            task_text = f"أرسل {DAILY_MESSAGE_TARGET} رسائل للبوت اليوم."
            db_manager.set_daily_task(uid, task_text)
            task = task_text
        bot.reply_to(message, f"📝 مهمتك اليومية:\n{task}")
        return

    # ======================
    # التحقق من إكمال المهمة (رسائل كمثال)
    # ======================
    # هنا نعتبر المهمة لإرسال رسائل
    if text != "فتح الصندوق":
        # زيادة عداد الرسائل اليومية
        db_manager.increment_messages(uid)
        return

    # ======================
    # فتح الصندوق
    # ======================
    if not db_manager.can_open_box(uid):
        bot.reply_to(message,
            "⏳ لم تكمل مهمتك بعد.\n"
            f"مهمتك الحالية:\n{db_manager.get_daily_task(uid)}"
        )
        return

    # منح صندوق الحظ إلى المخزون
    db_manager.set_box_opened(uid)
    reward = random.choice(BOX_REWARDS)
    db_manager.add_to_inventory(uid, reward)

    bot.reply_to(message,
        f"✅ تهانينا {first_name}!\n"
        f"تم إكمال مهمتك اليومية.\n"
        f"🎁 حصلت على صندوق الحظ! تمت إضافته إلى مخزونك.\n"
        f"اكتب 'مخزوني' لعرض كل ما لديك."
                )
