# ملف: cmd_birthdays.py
import telebot
import db_manager
import datetime
import time
from threading import Thread

COMMANDS = [
    "اضف عيد", "مسح عيد", "عيد ميلاد", "قائمه الاعياد",
    "تفعيل عيد ميلاد", "تعطيل عيد ميلاد"
]

CHECK_INTERVAL = 300  # 5 دقائق بالثواني

def handle(bot, message):
    text = message.text.strip()
    uid = message.from_user.id

    try:
        # ===== إضافة عيد ميلاد =====
        if text.startswith("اضف عيد"):
            parts = text.split()
            if len(parts) < 5:
                bot.reply_to(message, "❌ الصيغة: اضف عيد <ID المستخدم> <اليوم> <الشهر> [السنة]")
                return
            target_uid = int(parts[2])
            day = int(parts[3])
            month = int(parts[4])
            year = int(parts[5]) if len(parts) >= 6 else None

            result = db_manager.add_birthday(target_uid, day, month, year)
            if result["ok"]:
                bot.reply_to(message, f"✅ تم إضافة عيد الميلاد:\nUID: {target_uid}\nاليوم: {day}\nالشهر: {month}\nالسنة: {year}")
            else:
                bot.reply_to(message, result["error"])

        # ===== مسح عيد ميلاد =====
        elif text.startswith("مسح عيد"):
            parts = text.split()
            if len(parts) < 3:
                bot.reply_to(message, "❌ الصيغة: مسح عيد <ID المستخدم>")
                return
            target_uid = int(parts[2])
            db_manager.remove_birthday(target_uid)
            bot.reply_to(message, f"✅ تم مسح عيد الميلاد للمستخدم: {target_uid}")

        # ===== عرض عيد ميلاد شخص =====
        elif text.startswith("عيد ميلاد"):
            parts = text.split()
            if len(parts) < 3:
                bot.reply_to(message, "❌ الصيغة: عيد ميلاد <ID المستخدم>")
                return
            target_uid = int(parts[2])
            birthday = db_manager.get_birthday(target_uid)
            if birthday:
                bot.reply_to(
                    message,
                    f"🎂 عيد ميلاد المستخدم {target_uid}:\n"
                    f"اليوم: {birthday.get('day')}\n"
                    f"الشهر: {birthday.get('month')}\n"
                    f"السنة: {birthday.get('year')}"
                )
            else:
                bot.reply_to(message, "⚠️ لم يتم تسجيل عيد ميلاد لهذا المستخدم.")

        # ===== قائمة جميع الأعياد =====
        elif text == "قائمه الاعياد":
            birthdays = db_manager.list_birthdays()
            if not birthdays:
                bot.reply_to(message, "⚠️ لا يوجد أعياد ميلاد مسجلة.")
                return
            msg = "🎉 قائمة أعياد الميلاد:\n\n"
            for b in birthdays:
                bd = b["birthday"]
                msg += f"UID: {b['uid']} — {bd.get('day')}/{bd.get('month')}/{bd.get('year')}\n"
            bot.reply_to(message, msg)

        # ===== تفعيل / تعطيل الرد التلقائي =====
        elif text == "تفعيل عيد ميلاد":
            db_manager.enable_birthday_auto(uid)
            bot.reply_to(message, "✅ تم تفعيل الرد التلقائي لعيد ميلادك.")

        elif text == "تعطيل عيد ميلاد":
            db_manager.disable_birthday_auto(uid)
            bot.reply_to(message, "✅ تم تعطيل الرد التلقائي لعيد ميلادك.")

    except Exception as e:
        bot.reply_to(message, f"❌ حدث خطأ: {str(e)}")

# ======================
# دالة التحقق وإرسال التهاني
# ======================
def birthday_scheduler(bot):
    def run():
        while True:
            today = datetime.datetime.now()
            birthdays = db_manager.list_birthdays()
            for b in birthdays:
                bd = b["birthday"]
                if bd["day"] == today.day and bd["month"] == today.month:
                    user_uid = b["uid"]
                    if not db_manager.is_birthday_auto_enabled(user_uid):
                        continue

                    try:
                        # جلب معلومات المستخدم
                        try:
                            user_info = bot.get_chat(user_uid)
                            name = user_info.first_name
                            username = user_info.username
                            photo_url = None
                            photos = bot.get_user_profile_photos(user_uid)
                            if photos.total_count > 0:
                                file_id = photos.photos[0][-1].file_id
                                file_info = bot.get_file(file_id)
                                photo_url = f"https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}"
                        except:
                            name = "المستخدم"
                            username = "لا يوجد"
                            photo_url = None

                        # رسالة التهنئة
                        msg = f"🎉 كل عام وأنت بخير {name}!\n"
                        msg += f"UID: {user_uid}\n"
                        msg += f"Username: @{username}\n"
                        msg += f"عيد ميلاد سعيد! 🎂"

                        if photo_url:
                            bot.send_photo(user_uid, photo_url, caption=msg)
                        else:
                            bot.send_message(user_uid, msg)
                    except:
                        continue

            time.sleep(CHECK_INTERVAL)
    Thread(target=run, daemon=True).start()
