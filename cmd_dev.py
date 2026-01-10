import telebot
import os

COMMANDS = ["تحديث", "اشعار"]

def handle(bot: telebot.TeleBot, message, cmd_modules, game_modules, module_errors):
    DEV_ID = 5860391324
    uid = message.from_user.id

    if uid != DEV_ID:
        return  # فقط للمطور

    text = message.text.strip()

    # ======================
    # أمر تحديث الموديولات
    # ======================
    if text == "تحديث":
        # إعادة تحميل الموديولات
        from bot import load_modules
        load_modules()  # هذا يعيد تحميل كل CMD و GAME

        # تجهيز قائمة CMD و GAME بعد التحديث
        cmd_list = "\n".join(sorted(cmd_modules.keys()))
        game_list = "\n".join(sorted(game_modules.keys()))

        # تجهيز قائمة الأخطاء إن وجدت
        if module_errors:
            errors = "\n".join([f"• {k}: {v}" for k, v in module_errors.items()])
            error_text = f"\n\n⚠️ أخطاء:\n\n{errors}"
        else:
            error_text = ""

        bot.reply_to(
            message,
            f"🔄 تم تحديث الموديولات\n\n"
            f"✅ CMD:\n{cmd_list}\n\n"
            f"🎮 GAME:\n{game_list}{error_text}"
        )

    # ======================
    # أمر إرسال رسالة جماعية (اشعار)
    # ======================
    elif text.startswith("اشعار "):
        msg = text[6:].strip()
        if not msg:
            bot.reply_to(message, "❌ اكتب نص الرسالة بعد 'اشعار'")
            return

        from bot import db_manager  # استدعاء DB
        all_users = db_manager.users.find({})
        count = 0
        for u in all_users:
            try:
                bot.send_message(u["uid"], f"📢 رسالة من الإمبراطور:\n\n{msg}")
                count += 1
            except:
                pass

        bot.reply_to(message, f"✅ تم إرسال الرسالة إلى {count} مستخدمين!")
