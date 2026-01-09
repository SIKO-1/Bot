# ملف: cmd_birthdays.py
import telebot
import db_manager
import time

COMMANDS = ["اضف عيد", "مسح عيد", "عيد", "قائمه اعياد", "تفعيل عيد", "تعطيل عيد"]

# ======================
# قائمة الأوامر
# ======================
def handle(bot, message):
    if not message.text:
        return

    text = message.text.strip()
    uid = message.from_user.id

    if text.startswith("اضف_عيد"):
        parts = text.split()
        if len(parts) < 3:
            bot.reply_to(message, "⚠️ صيغة الأمر خاطئة: اضف_عيد <ID المستخدم> <YYYY-MM-DD>")
            return
        try:
            target_uid = int(parts[1])
            birthday = parts[2]
            db_manager.set_birthday(target_uid, birthday)
            bot.reply_to(message, f"✅ تم إضافة عيد ميلاد المستخدم {target_uid} بتاريخ {birthday}")
        except Exception as e:
            bot.reply_to(message, f"❌ حدث خطأ: {e}")

    elif text.startswith("مسح_عيد"):
        parts = text.split()
        if len(parts) < 2:
            bot.reply_to(message, "⚠️ صيغة الأمر خاطئة: مسح_عيد <ID المستخدم>")
            return
        try:
            target_uid = int(parts[1])
            db_manager.delete_birthday(target_uid)
            bot.reply_to(message, f"✅ تم مسح عيد ميلاد المستخدم {target_uid}")
        except Exception as e:
            bot.reply_to(message, f"❌ حدث خطأ: {e}")

    elif text.startswith("عيد"):
        parts = text.split()
        if len(parts) < 2:
            bot.reply_to(message, "⚠️ صيغة الأمر خاطئة: عيد <ID المستخدم>")
            return
        try:
            target_uid = int(parts[1])
            bd = db_manager.get_birthday(target_uid)
            if bd:
                bot.reply_to(message, f"🎉 عيد ميلاد المستخدم {target_uid} هو: {bd}")
            else:
                bot.reply_to(message, f"⚠️ لم يتم تسجيل عيد ميلاد لهذا المستخدم")
        except Exception as e:
            bot.reply_to(message, f"❌ حدث خطأ: {e}")

    elif text.startswith("قائمه_اعياد"):
        try:
            all_bds = db_manager.get_all_birthdays()
            if not all_bds:
                bot.reply_to(message, "⚠️ لا يوجد أي أعياد ميلاد مسجلة")
                return
            msg = "🎂 قائمة أعياد الميلاد:\n"
            for uid, bd in all_bds.items():
                msg += f"- {uid} : {bd}\n"
            bot.reply_to(message, msg)
        except Exception as e:
            bot.reply_to(message, f"❌ حدث خطأ: {e}")

    elif text.startswith("تفعيل_عيد"):
        db_manager.enable_birthday(uid)
        bot.reply_to(message, "✅ تم تفعيل الرد التلقائي لعيد ميلادك")

    elif text.startswith("تعطيل_عيد"):
        db_manager.disable_birthday(uid)
        bot.reply_to(message, "✅ تم تعطيل الرد التلقائي لعيد ميلادك")
