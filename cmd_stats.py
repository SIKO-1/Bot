from db_manager import (
    _get_user, get_all_users_count,
    update_user_gold, users
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

        name_display = user.get('name') or str(user.get('uid'))
        username_display = f"@{user.get('username')}" if user.get('username') else str(user.get('uid'))

        report = f"""╔═════════════════╗
أهلاً بك في إدارة المستخدمين
╚═════════════════╝

عدد المستخدمين الكلي: {get_all_users_count()}

━━━━━━━━━━━━━━━
معلوماتك:

• الاسم: {name_display}
• يوزرنيم / UID: {username_display}
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

        target_name = target_user.get('name') or str(target_user.get('uid'))
        target_username = f"@{target_user.get('username')}" if target_user.get('username') else str(target_user.get('uid'))

        bot.reply_to(
            message,
            f"💰 سحب {amount} ذهب من {target_name} / {target_username}\nالرصيد الجديد: {new_gold}"
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
            name_display = u.get('name') or str(u.get('uid'))
            username_display = f"@{u.get('username')}" if u.get('username') else str(u.get('uid'))
            report += f"{i}- {name_display} / {username_display} / ذهب: {u.get('gold',0)}\n"

        report += "\n━━━━━━━━━━━━━━━\nأكثر 5 أشخاص تفاعلاً:\n\n"
        for i, u in enumerate(active, 1):
            name_display = u.get('name') or str(u.get('uid'))
            report += f"{i}- {name_display} / رسائل: {u.get('total_messages',0)}\n"
        report += "━━━━━━━━━━━━━━━"
        bot.reply_to(message, report)
        return

# ======================
# دالة مساعدة للحصول على كل المستخدمين
# ======================
def _get_all_users_list():
    return list(users.find({}))
