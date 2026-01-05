# ملف: cmd_users_admin.py
import telebot
import db_manager
import time

COMMANDS = ["ادارة_المستخدمين", "users_admin", "المستخدمين"]

def handle(bot, message):
    # فقط المطور يقدر يستخدم الأمر
    DEV_ID = 5860391324
    if message.from_user.id != DEV_ID:
        return

    if message.text not in COMMANDS and not message.text.startswith("سحب"):
        return

    user_name = message.from_user.first_name
    text = message.text

    # =========================
    # قائمة المستخدمين وإحصائياتهم
    # =========================
    if text in ["ادارة_المستخدمين", "users_admin", "المستخدمين"]:
        all_users = db_manager.users.find()
        total_users = db_manager.users.count_documents({})
        reply = f"👑 إدارة المستخدمين الإمبراطوريين\n"
        reply += f"⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻\n"
        reply += f"عدد المستخدمين الكلي: {total_users}\n\n"
        reply += f"📊 احصائيات بعض المستخدمين:\n"
        for user in all_users.limit(20):  # نعرض أول 20 مستخدم
            uid = user["uid"]
            gold = user.get("gold", 0)
            bank = user.get("bank", 0)
            banned = "✅" if user.get("banned", False) else "❌"
            reply += f"• UID {uid} — ذهب: {gold}, بنك: {bank}, محظور: {banned}\n"
        bot.reply_to(message, reply)

    # =========================
    # سحب رصيد من مستخدم
    # صيغة: سحب <UID> <المبلغ>
    # =========================
    elif text.startswith("سحب"):
        parts = text.split()
        if len(parts) < 3:
            return bot.reply_to(message, "⚠️ صيغة خاطئة! مثال: سحب 5860391324 500")
        try:
            uid = int(parts[1])
            amount = int(parts[2])
        except:
            return bot.reply_to(message, "❌ UID أو المبلغ يجب أن يكون رقم صحيح!")

        user_gold = db_manager.get_user_gold(uid)
        if amount > user_gold:
            return bot.reply_to(message, f"⚠️ لا يمكن سحب {amount} ذهب، رصيد المستخدم {user_gold} فقط!")

        db_manager.update_user_gold(uid, -amount)
        bot.reply_to(message, f"✅ تم سحب {amount} ذهب من المستخدم UID {uid} بنجاح!")
