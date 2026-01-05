from db_manager import (
    _get_user, get_all_users_count,
    update_user_gold
)
from operator import itemgetter

COMMANDS = ["احصائيات", "سحب", "تصنيف"]

def handle(bot, message):
    text = message.text.strip()
    uid = message.from_user.id

    if not any(text.startswith(cmd) for cmd in COMMANDS):
        return

    # ======================
    # احصائيات المستخدم
    # ======================
    if text.startswith("احصائيات"):
        user = _get_user(uid)
        gold = user.get("gold", 0)
        bank = user.get("bank", 0)
        msgs = user.get("total_messages", 0)
        daily = user.get("daily_usage", 0)
        banned = "✅" if not user.get("banned", False) else "❌"

        report = f"""╔═════════════════╗
أهلاً بك في إدارة المستخدمين
╚═════════════════╝

عدد المستخدمين الكلي: {get_all_users_count()}

━━━━━━━━━━━━━━━
معلوماتك:

• الاسم: {user.get('name') or 'غير معروف'}
• يوزرنيم: @{user.get('username') or 'لا يوجد'}
• الذهب: {gold}
• البنك: {bank}
• عدد الرسائل الكلي: {msgs}
• الاستخدام اليومي: {daily}
• محظور: {banned}
━━━━━━━━━━━━━━━
"""
        bot.reply_to(message, report)
        return

    # ======================
    # سحب الذهب
    # ======================
    if text.startswith("سحب"):
        parts = text.split()
        if len(parts) != 3:
            bot.reply_to(message, "❌ صيغة الأمر: سحب <UID> <المبلغ>")
            return
        try:
            target_uid = int(parts[1])
            amount = int(parts[2])
        except ValueError:
            bot.reply_to(message, "❌ يجب أن يكون UID والمبلغ أرقاماً صحيحة")
            return

        target_user = _get_user(target_uid)
        old_gold = target_user.get("gold", 0)
        new_gold = max(0, old_gold - amount)
        update_user_gold(target_uid, -amount)
        bot.reply_to(
            message,
            f"💰 سحب {amount} ذهب من {target_user.get('name') or 'غير معروف'} / @{target_user.get('username') or 'لا يوجد'}\nالرصيد الجديد: {new_gold}"
        )
        return

    # ======================
    # قائمة التصنيف
    # ======================
    if text.startswith("تصنيف"):
        all_users = list(_get_all_users_list())
        # أغنى 5 أشخاص
        richest = sorted(all_users, key=lambda u: u.get("gold", 0), reverse=True)[:5]
        # أكثر 5 تفاعلاً
        active = sorted(all_users, key=lambda u: u.get("total_messages", 0), reverse=True)[:5]

        report = "╔═════════════════╗\n   قائمة التصنيف\n╚═════════════════╝\n\n"

        report += "أغنى 5 أشخاص بالبوت:\n\n"
        for i, u in enumerate(richest, 1):
            report += f"{i}- {u.get('name') or 'غير معروف'} / @{u.get('username') or 'لا يوجد'} / ذهب: {u.get('gold',0)}\n"
        report += "\n━━━━━━━━━━━━━━━\nأكثر 5 أشخاص تفاعلاً:\n\n"
        for i, u in enumerate(active, 1):
            report += f"{i}- {u.get('name') or 'غير معروف'} / رسائل: {u.get('total_messages',0)}\n"
        report += "━━━━━━━━━━━━━━━"
        bot.reply_to(message, report)
        return

# ======================
# دالة مساعدة للحصول على كل المستخدمين
# ======================
def _get_all_users_list():
    from db_manager import users  # جلب الـ collection
    return list(users.find({}))
