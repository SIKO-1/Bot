# ملف: cmd_stats.py
import db_manager
from telebot.types import Message

COMMANDS = ["احصائيات", "سحب", "تصنيف"]

# ======================
# إدارة الإحصائيات
# ======================
def handle(bot, message: Message):
    text = message.text.strip()
    uid = message.from_user.id
    user_name = message.from_user.first_name

    # ======================
    # احصائيات المستخدم
    # ======================
    if text == "احصائيات":
        users = db_manager.get_all_users()
        total_users = len(users)

        report = "╔═════════════════╗\n"
        report += f"  أهلاً بك يا : {user_name} في إدارة الإحصائيات\n"
        report += "╚═════════════════╝\n\n"

        report += f"عدد المستخدمين الكلي: {total_users}\n\n"
        report += "📊 احصائيات المستخدمين:\n"

        for u in users:
            report += f"• UID {u['uid']} — ذهب: {u['gold']}, بنك: {u['bank']}, محظور: {'✅' if u['banned'] else '❌'}\n"

        bot.reply_to(message, report)
        return

    # ======================
    # سحب ذهب من مستخدم
    # ======================
    if text.startswith("سحب"):
        parts = text.split()
        if len(parts) < 3:
            return bot.reply_to(message, "⚠️ مثال: سحب 8438522384 200 أو رد على رسالة المستخدم: سحب 200")

        # تحديد المبلغ
        try:
            if message.reply_to_message:
                target_uid = message.reply_to_message.from_user.id
                amount = int(parts[1])
            else:
                target_uid = int(parts[1])
                amount = int(parts[2])
        except:
            return bot.reply_to(message, "❌ خطأ في كتابة الأوامر!")

        target_gold = db_manager.get_user_gold(target_uid)
        if amount > target_gold:
            return bot.reply_to(message, f"⚠️ رصيد المستخدم {target_gold} ذهب فقط!")

        db_manager.update_user_gold(target_uid, -amount)
        db_manager.update_user_gold(uid, amount)

        bot.reply_to(message,
            f"✅ تم سحب {amount} ذهب من UID {target_uid} بنجاح!\n"
            f"💰 رصيدك الحالي: {db_manager.get_user_gold(uid)}"
        )
        return

    # ======================
    # قائمة التصنيف
    # ======================
    if text == "تصنيف":
        users = db_manager.get_all_users()

        # أغنى 5 أشخاص
        richest = sorted(users, key=lambda x: x["gold"], reverse=True)[:5]
        # أكثر 5 تفاعلاً (عدد استخدام الأوامر + الألعاب)
        active = sorted(users, key=lambda x: x.get("messages_count", 0), reverse=True)[:5]

        report = "╔═════════════════╗\n"
        report += "   قائمة التصنيف\n"
        report += "╚═════════════════╝\n\n"

        report += "أغنى 5 أشخاص بالبوت:\n"
        for i, u in enumerate(richest, 1):
            report += f"{i}- {u.get('name','غير معروف')} / @{u.get('username','لايوجد')} / ({u['gold']} ذهب)\n"

        report += "\n━━━━━━━━━━━━━━\n"
        report += "أكثر 5 أشخاص تفاعلاً:\n"
        for i, u in enumerate(active, 1):
            report += f"{i}- {u.get('name','غير معروف')} / ({u.get('messages_count',0)} رسالة)\n"

        report += "━━━━━━━━━━━━━━━"
        bot.reply_to(message, report)
        return
