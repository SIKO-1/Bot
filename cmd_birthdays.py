# ملف: cmd_birthdays.py
import telebot
import db_manager

COMMANDS = ["اضف عيد", "مسح عيد", "قائمة الأعياد"]

def handle(bot, message):
    text = message.text.strip()
    uid = message.from_user.id

    if not any(text.startswith(cmd) for cmd in COMMANDS):
        return

    # ======= إضافة عيد ميلاد =======
    if text.startswith("اضف عيد"):
        try:
            parts = text.split()
            if len(parts) != 4:
                bot.reply_to(message, "❌ صيغة خاطئة. استخدم:\nاضف عيد <id> <yyyy-mm-dd>")
                return

            user_id = int(parts[2])
            birth_date = parts[3]

            result = db_manager.add_birthday(user_id, birth_date)
            if result:
                bot.reply_to(message, f"✅ تم إضافة عيد الميلاد للمستخدم {user_id}: {birth_date}")
            else:
                bot.reply_to(message, f"❌ حدث خطأ أثناء إضافة عيد الميلاد.")
        except Exception as e:
            bot.reply_to(message, f"❌ حدث خطأ: {e}")

    # ======= مسح عيد ميلاد =======
    elif text.startswith("مسح عيد"):
        try:
            parts = text.split()
            if len(parts) != 3:
                bot.reply_to(message, "❌ صيغة خاطئة. استخدم:\nمسح عيد <id>")
                return

            user_id = int(parts[2])
            result = db_manager.remove_birthday(user_id)
            if result:
                bot.reply_to(message, f"✅ تم مسح عيد الميلاد للمستخدم {user_id}")
            else:
                bot.reply_to(message, "⚠️ لم يتم العثور على عيد ميلاد لهذا المستخدم.")
        except Exception as e:
            bot.reply_to(message, f"❌ حدث خطأ: {e}")

    # ======= عرض قائمة الأعياد =======
    elif text == "قائمة الأعياد":
        try:
            birthdays = db_manager.get_all_birthdays()
            if not birthdays:
                bot.reply_to(message, "⚠️ لا توجد أعياد ميلاد مسجلة حالياً.")
                return

            reply = "🎂 قائمة الأعياد المسجلة:\n"
            for b in birthdays:
                reply += f"- {b['uid']} : {b['birth_date']}\n"
            bot.reply_to(message, reply)
        except Exception as e:
            bot.reply_to(message, f"❌ حدث خطأ: {e}")
