# ملف: cmd_ban.py
import time
import db_manager  # الربط مع MongoDB
from telebot import types

COMMANDS_BAN = ["حظر", "عفو", "قائمة المحظورين"]

# هنا نحدد ايديه المطور
DEVELOPER_ID = 5860391324

def handle(bot, message):
    uid = message.from_user.id
    text = message.text

    # ======== التحقق من الحظر قبل أي شيء =========
    banned_users = db_manager.get_banned_users()
    if uid in banned_users and uid != DEVELOPER_ID:
        return bot.reply_to(message, "⛔️ اُصمت! جاء أمر من الإمبراطور بنفيك خارج مملكته!")

    # ======== أوامر الحظر للمطور فقط =========
    if uid != DEVELOPER_ID:
        return  # أي شخص غير المطور ما يقدر يستخدم أوامر الحظر

    # ======== أمر الحظر =========
    if text.startswith("حظر"):
        if not message.reply_to_message:
            return bot.reply_to(message, "⚠️ للـحظر، الرجاء الرد على رسالة الشخص المراد حظره.")
        target_id = message.reply_to_message.from_user.id
        if target_id == DEVELOPER_ID:
            return bot.reply_to(message, "🚫 ما تقدر تحظر الإمبراطور!")
        db_manager.ban_user(target_id)
        bot.reply_to(message, f"✅ تم حظر المستخدم: {target_id}")

    # ======== أمر العفو =========
    elif text.startswith("عفو"):
        if not message.reply_to_message:
            return bot.reply_to(message, "⚠️ للعفو، الرجاء الرد على رسالة الشخص المراد رفع الحظر عنه.")
        target_id = message.reply_to_message.from_user.id
        db_manager.unban_user(target_id)
        bot.reply_to(message, f"🎉 بأمر من الإمبراطور تم العفو عنك! {target_id}")

    # ======== قائمة المحظورين =========
    elif text.startswith("قائمة المحظورين"):
        banned_list = db_manager.get_banned_users()
        if not banned_list:
            return bot.reply_to(message, "✅ لا يوجد أي محظورين حالياً.")
        banned_text = "📜 قائمة المحظورين:\n" + "\n".join([str(i) for i in banned_list])
        bot.reply_to(message, banned_text)
