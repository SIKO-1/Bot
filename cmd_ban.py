# ملف: cmd_ban.py
import telebot

DEVELOPER_ID = 5860391324

# قائمة الحظر داخل ذاكرة البوت
banned_users = set()

COMMANDS = ["حظر", "عفو", "قائمة_المحظورين"]

def handle(bot, message):
    global banned_users

    uid = message.from_user.id

    # 1️⃣ التحقق من المحظورين
    if uid in banned_users and uid != DEVELOPER_ID:
        bot.reply_to(message, "اُصمت! جاء أمر من الإمبراطور بنفيك خارج مملكته! 👑")
        return

    # 2️⃣ الأوامر الخاصة بالمطور فقط
    if uid != DEVELOPER_ID:
        return

    text = message.text.split()
    cmd = text[0]

    # ===== حظر شخص بالرد =====
    if cmd == "حظر":
        if not message.reply_to_message:
            bot.reply_to(message, "❌ يجب الرد على رسالة الشخص الذي تريد حظره!")
            return
        target_uid = message.reply_to_message.from_user.id
        banned_users.add(target_uid)
        bot.reply_to(message, f"✅ تم حظر المستخدم {message.reply_to_message.from_user.first_name} من مملكة البوت 👑")
        return

    # ===== عفو عن شخص بالرد =====
    if cmd == "عفو":
        if not message.reply_to_message:
            bot.reply_to(message, "❌ يجب الرد على رسالة الشخص الذي تريد العفو عنه!")
            return
        target_uid = message.reply_to_message.from_user.id
        if target_uid in banned_users:
            banned_users.discard(target_uid)
            bot.reply_to(message, f"✅ تم العفو عن المستخدم {message.reply_to_message.from_user.first_name} 👑")
            bot.send_message(target_uid, "بأمر من الإمبراطور تم العفو عنك، اشكره! 👑")
        else:
            bot.reply_to(message, "⚠️ هذا الشخص ليس محظوراً بالفعل!")
        return

    # ===== عرض قائمة المحظورين =====
    if cmd == "قائمة_المحظورين":
        if not banned_users:
            bot.reply_to(message, "📜 لا يوجد مستخدمين محظورين حالياً.")
            return
        text_list = "📜 قائمة المحظورين الحاليين:\n"
        for u in banned_users:
            text_list += f"• {u}\n"
        bot.reply_to(message, text_list)
        return
