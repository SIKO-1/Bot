# ملف: cmd_dev_recharge.py
import telebot
import db_manager

# ضع هنا أيديك
DEVELOPER_ID = 5860391324

COMMANDS = ["شحن", "شحن_ذهب"]

def handle(bot, message):
    if message.from_user.id != DEVELOPER_ID:
        return  # فقط المطور يقدر يستخدم

    if message.text.split()[0] not in COMMANDS:
        return

    if not message.reply_to_message:
        bot.reply_to(message, "❌ يجب الرد على رسالة الشخص الذي تريد شحنه الذهب!")
        return

    parts = message.text.split()
    if len(parts) < 2:
        bot.reply_to(message, "❌ اكتب المبلغ بعد الامر. مثال: شحن 5000")
        return

    try:
        amount = int(parts[1])
    except ValueError:
        bot.reply_to(message, "❌ يرجى كتابة الرقم بالأرقام فقط!")
        return

    target_user = message.reply_to_message.from_user
    uid = target_user.id

    # شحن الذهب
    new_gold = db_manager.update_user_gold(uid, amount)

    bot.reply_to(message,
        f"✅ تم شحن {amount} ذهب للمستخدم {target_user.first_name} 👑\n"
        f"💰 رصيده الآن: {new_gold} ذهب"
                )
