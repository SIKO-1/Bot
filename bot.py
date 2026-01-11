import telebot
import os

def handle(bot: telebot.TeleBot, message, cmd_modules=None, game_modules=None, module_errors=None):
    DEV_ID = 5860391324
    uid = message.from_user.id

    if uid != DEV_ID:
        return  # فقط للمطور

    text = message.text.strip()

    # ======================
    # أمر إرسال رسالة جماعية (اشعار)
    # ======================
    if text.startswith("اشعار "):
        msg = text[6:].strip()
        if not msg:
            bot.reply_to(message, "❌ اكتب نص الرسالة بعد 'اشعار'")
            return

        # استدعاء DB
        from bot import db_manager
        all_users = db_manager.users.find({})
        count = 0
        for u in all_users:
            try:
                bot.send_message(u["uid"], f"📢 رسالة من الإمبراطور:\n\n{msg}")
                count += 1
            except:
                pass

        bot.reply_to(message, f"✅ تم إرسال الرسالة إلى {count} مستخدمين!")
