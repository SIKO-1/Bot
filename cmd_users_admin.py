# ملف: cmd_users_admin.py
import db_manager

# ضع آيدي المطور هنا
DEVELOPER_ID = 5860391324  # ← غيره لآيديك

COMMANDS = [
    "مستخدم",
    "ادارة مستخدم",
    "ادارة المستخدم"
]

def handle(bot, message):
    uid = message.from_user.id

    # حماية: للمطور فقط
    if uid != DEVELOPER_ID:
        return

    text = message.text.strip()

    # ======================
    # عرض معلومات مستخدم (بالرد)
    # ======================
    if text.startswith("مستخدم") and message.reply_to_message:
        target = message.reply_to_message.from_user
        tid = target.id

        gold = db_manager.get_user_gold(tid)
        banned = db_manager.is_user_banned(tid)
        inventory = db_manager.get_inventory(tid)

        info = (
            "╔═════════════════╗\n"
            "   إدارة المستخدم\n"
            "╚═════════════════╝\n\n"
            f"👤 الاسم : {target.first_name}\n"
            f"🆔 الايدي : {tid}\n"
            f"💰 الذهب : {gold}\n"
            f"🚫 محظور : {'نعم' if banned else 'لا'}\n"
            f"🎒 العناصر : {len(inventory)}\n"
        )
        bot.reply_to(message, info)
        return

    # ======================
    # حظر مستخدم (بالرد)
    # ======================
    if text == "بان" and message.reply_to_message:
        tid = message.reply_to_message.from_user.id
        db_manager.ban_user(tid)
        bot.reply_to(message, "⛔ تم نفي المستخدم خارج الإمبراطورية.")
        return

    # ======================
    # عفو (رفع الحظر)
    # ======================
    if text == "الغاء بان" and message.reply_to_message:
        tid = message.reply_to_message.from_user.id
        db_manager.unban_user(tid)
        try:
            bot.send_message(
                tid,
                "🕊️ عفو عام\n\n"
                "بأمر من الإمبراطور تم العفو عنك.\n"
                "أحسن السلوك ولا تختبر الصبر مرة أخرى."
            )
        except:
            pass
        bot.reply_to(message, "✅ تم العفو عن المستخدم.")
        return

    # ======================
    # شحن (بالرد + رقم)
    # ======================
    if text.startswith("شحن") and message.reply_to_message:
        parts = text.split()
        if len(parts) != 2:
            bot.reply_to(message, "❌ الصيغة: شحن 1000")
            return

        try:
            amount = int(parts[1])
        except:
            bot.reply_to(message, "❌ اكتب رقم صحيح.")
            return

        tid = message.reply_to_message.from_user.id
        db_manager.update_user_gold(tid, amount)
        bot.reply_to(
            message,
            f"💰 تم شحن {amount} ذهبة للمستخدم."
        )
        return

    # ======================
    # قائمة الحظر
    # ======================
    if text == "قائمة الحظر":
        banned = db_manager.get_banned_users()
        if not banned:
            bot.reply_to(message, "✅ لا يوجد محظورين.")
            return

        msg = "🚫 قائمة المنفيين:\n\n"
        for u in banned:
            msg += f"- {u}\n"

        bot.reply_to(message, msg)
        return
