# ملف: cmd_birthdays.py
import telebot
import db_manager  # تأكد من وجود db_manager.py وأنه محدث
import time
from threading import Thread

COMMANDS = ["اضف عيد ميلاد", "مسح عيد ميلاد", "عيد ميلاد", "مسح قائمه الاعياد", "تفعيل عيد ميلاد", "تعطيل عيد ميلاد"]
DEV_IDS = [5690109912] [5951199025] [5860391324]  # المطورين اللي يقدرون يستخدمون الأوامر

# ======================
# متغير تفعيل/تعطيل
# ======================
birthdays_enabled = False
check_interval = 300  # كل 5 دقائق

# ======================
# تفعيل/تعطيل
# ======================
def enable_birthdays():
    global birthdays_enabled
    birthdays_enabled = True

def disable_birthdays():
    global birthdays_enabled
    birthdays_enabled = False

# ======================
# دالة تحقق يوم الميلاد
# ======================
def birthday_scheduler(bot):
    def run():
        while True:
            if birthdays_enabled:
                all_users = db_manager.get_all_users()  # افترض عندك دالة ترجع كل المستخدمين
                today = time.strftime("%d-%m")
                for user in all_users:
                    if "birthday" in user and user["birthday"] == today:
                        chat_id = user["uid"]
                        name = user.get("name", "صديقنا")
                        bio = user.get("bio", "لا يوجد")
                        username = user.get("username", "لا يوجد")
                        msg = f"🎉 عيد ميلاد سعيد يا {name}!\n\n• معرف: @{username}\n• الايدي: {chat_id}\n• البايو: {bio}"
                        bot.send_message(chat_id, msg)
            time.sleep(check_interval)
    Thread(target=run, daemon=True).start()

# ======================
# التعامل مع الرسائل
# ======================
def handle(bot, message):
    text = message.text
    uid = message.from_user.id

    if not any(cmd in text for cmd in COMMANDS):
        return

    # التحقق من صلاحية المستخدم
    if uid not in DEV_IDS:
        bot.reply_to(message, "❌ هذا الأمر للمطور فقط")
        return

    # ===== تفعيل / تعطيل =====
    if text == "تفعيل عيد ميلاد":
        enable_birthdays()
        bot.reply_to(message, "✅ تم تفعيل تهاني عيد الميلاد")
        return
    if text == "تعطيل عيد ميلاد":
        disable_birthdays()
        bot.reply_to(message, "🔴 تم تعطيل تهاني عيد الميلاد")
        return

    # ===== إضافة عيد ميلاد =====
    if text.startswith("اضف عيد ميلاد"):
        try:
            parts = text.split()
            user_id = int(parts[2])  # ID المستخدم
            date = parts[3]  # صيغة: يوم-شهر مثلا 09-01
            db_manager.set_user_birthday(user_id, date)
            bot.reply_to(message, f"✅ تم إضافة عيد ميلاد للمستخدم {user_id} بتاريخ {date}")
        except:
            bot.reply_to(message, "⚠️ الصيغة خاطئة! استخدم: اضف عيد ميلاد <id> <dd-mm>")
        return

    # ===== مسح عيد ميلاد =====
    if text.startswith("مسح عيد ميلاد"):
        try:
            parts = text.split()
            user_id = int(parts[2])
            db_manager.delete_user_birthday(user_id)
            bot.reply_to(message, f"✅ تم مسح عيد ميلاد المستخدم {user_id}")
        except:
            bot.reply_to(message, "⚠️ الصيغة خاطئة! استخدم: مسح عيد ميلاد <id>")
        return

    # ===== عرض قائمة الأعياد =====
    if text == "عيد ميلاد":
        all_birthdays = db_manager.get_all_birthdays()
        if not all_birthdays:
            bot.reply_to(message, "لا توجد أعياد ميلاد مسجلة.")
            return
        msg = "🎂 قائمة الأعياد:\n\n"
        for b in all_birthdays:
            msg += f"• ID: {b['uid']} — تاريخ: {b['birthday']}\n"
        bot.reply_to(message, msg)
        return

    # ===== مسح قائمة الأعياد =====
    if text == "مسح قائمه الاعياد":
        db_manager.clear_all_birthdays()
        bot.reply_to(message, "✅ تم مسح جميع الأعياد")
        return
