import db_manager
from telebot import types

# أوامر الحظر والعفو
COMMANDS_BAN = ["حظر"]
COMMANDS_PARDON = ["عفو"]
COMMANDS_LIST = ["قائمة الحظر", "الحظر"]

def handle(bot, message):
    uid = message.from_user.id
    user_name = message.from_user.first_name
    text = message.text

    # ====== أوامر الحظر من المطور فقط ======
    if text.startswith(tuple(COMMANDS_BAN)):
        if uid != 5860391324:  # مطور الإمبراطورية
            return
        if not message.reply_to_message:
            bot.reply_to(message, "⚠️ الرجاء الرد على رسالة الشخص الذي تريد حظره!")
            return

        target_id = message.reply_to_message.from_user.id
        db_manager.ban_user(target_id)
        bot.reply_to(message, f"👑 {user_name} أمر الإمبراطور: تم حظر الشخص بنجاح!")
        return

    # ====== أوامر العفو من المطور فقط ======
    if text.startswith(tuple(COMMANDS_PARDON)):
        if uid != 5860391324:
            return
        if not message.reply_to_message:
            bot.reply_to(message, "⚠️ الرجاء الرد على رسالة الشخص الذي تريد العفو عنه!")
            return

        target_id = message.reply_to_message.from_user.id
        db_manager.unban_user(target_id)
        bot.reply_to(message, f"👑 {user_name} أمر الإمبراطور: تم العفو عن الشخص!")

        # رسالة عفو للشخص العفو عنه
        try:
            bot.send_message(target_id, "👑 تم العفو عنك بأمر الإمبراطور! اشكر الإمبراطور 🌟")
        except:
            pass
        return

    # ====== عرض قائمة الحظر ======
    if text in COMMANDS_LIST:
        if uid != 5860391324:
            bot.reply_to(message, "❌ هذا الأمر للمطور فقط!")
            return

        banned_users = db_manager.get_banned_users()
        if not banned_users:
            bot.reply_to(message, "📜 لا يوجد أي شخص محظور حالياً.")
            return

        text_list = "📜 قائمة المحظورين:\n\n"
        for u in banned_users:
            text_list += f"👤 ID: {u}\n"
        bot.reply_to(message, text_list)
        return

    # ====== الصمت العقابي لأي شخص محظور ======
    if db_manager.is_user_banned(uid):
        # حذف الرسالة إذا كانت موجودة
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except:
            pass
        # الصمت العقابي الكامل: لا يرد أبداً
        return
