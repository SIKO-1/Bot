import db_manager
import telebot

COMMANDS = ["رست", "اشعار"]

def handle(bot: telebot.TeleBot, message):
    DEV_ID = 5860391324
    uid = message.from_user.id

    if uid != DEV_ID:
        return  # فقط للمطور

    text = message.text.strip()

    # ======================
    # أمر Reset البوت
    # ======================
    if text.lower() == "رست":
        db_manager.reset_daily_usage()  # إعادة ضبط البيانات اليومية
        # ممكن تضيف أي Reset آخر هنا
        bot.reply_to(message, "♻️ تم إعادة تشغيل البوت بنجاح!")
        bot.send_message(DEV_ID, "✅ البوت تم تشغيله بعد الرست.")

    # ======================
    # أمر إرسال رسالة جماعية
    # ======================
    elif text.lower().startswith("اشعار "):
        msg = text[6:].strip()
        if not msg:
            bot.reply_to(message, "❌ اكتب نص الرسالة بعد 'اشعار'")
            return

        all_users = db_manager.users.find({})
        count = 0
        for u in all_users:
            try:
                bot.send_message(u["uid"], f"📢 رسالة من الإمبراطور:\n\n{msg}")
                count += 1
            except:
                pass

        bot.reply_to(message, f"✅ تم إرسال الرسالة إلى {count} مستخدمين!")
