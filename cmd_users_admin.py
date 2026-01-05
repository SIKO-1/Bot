# ملف: cmd_users_admin.py
import telebot
import db_manager

COMMANDS = ["ادارة_المستخدمين", "مستخدمين", "stats", "احصائيات", "سحب"]

def handle(bot, message):
    DEV_ID = 5860391324
    if message.from_user.id != DEV_ID:
        return bot.reply_to(message, "❌ أنت لست المطور!")

    parts = message.text.split()
    if len(parts) < 2:
        return bot.reply_to(message,
            "⚠️ استخدم:\n"
            "• احصائيات <id>\n"
            "• سحب <id> <المبلغ>"
        )

    command = parts[1].lower()

    # ======================
    # احصائيات مستخدم
    # ======================
    if command in ["احصائيات", "stats"] and len(parts) >= 3:
        uid = int(parts[2])
        stats = db_manager.get_user_stats(uid)
        text = (
            f"📊 احصائيات المستخدم {uid}:\n"
            f"💰 الذهب: {stats['gold']}\n"
            f"🏦 البنك: {stats['bank']}\n"
            f"🎒 المخزون: {', '.join(stats['inventory']) if stats['inventory'] else 'فارغ'}\n"
            f"📨 الرسائل الكلية: {stats['total_messages']}\n"
            f"⏱ الاستخدام اليومي: {stats['daily_usage']}\n"
            f"🚫 محظور: {'نعم' if stats['banned'] else 'لا'}"
        )
        bot.reply_to(message, text)

    # ======================
    # سحب رصيد
    # ======================
    elif command == "سحب" and len(parts) >= 4:
        uid = int(parts[2])
        try:
            amount = int(parts[3])
        except:
            return bot.reply_to(message, "❌ المبلغ يجب أن يكون رقم صحيح!")

        db_manager.update_user_gold(uid, -amount)
        bot.reply_to(message, f"✅ تم سحب {amount} ذهب من المستخدم {uid}")

    else:
        bot.reply_to(message, "⚠️ أمر غير معروف أو ناقص المعطيات")
