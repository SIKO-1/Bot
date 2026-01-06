import db_manager

COMMANDS = ["ادارة_المستخدمين", "المستخدمين"]

MAX_MSG_LENGTH = 4000  # الحد الأقصى لرسائل Telegram

def handle(bot, message):
    if message.text not in COMMANDS:
        return

    if message.from_user.id != 5860391324:
        bot.reply_to(message, "❌ هذا الأمر للمطور فقط")
        return

    users = list(db_manager.users.find({}))
    total = len(users)

    banned = []
    active = []

    for user in users:
        uid = user.get("uid")
        gold = user.get("gold", 0)
        bank = user.get("bank", 0)
        is_banned = user.get("banned", False)

        info = f"- ID: {uid} | 💰 {gold} | 🏦 {bank}"
        if is_banned:
            banned.append(info + " | 🚫 محظور")
        else:
            active.append(info)

    text_header = (
        "╔═════════════════╗\n"
        f"  أهلاً بك يا {message.from_user.first_name} في إدارة المستخدمين\n"
        "╚═════════════════╝\n\n"
        f"👥 عدد المستخدمين الكلي: {total}\n\n"
        "🚫 المحظورين:\n"
    )

    text_banned = "\n".join(banned) if banned else "— لا يوجد —"
    text_active = "\n\n✅ غير المحظورين:\n" + ("\n".join(active) if active else "— لا يوجد —")

    full_text = text_header + text_banned + text_active

    # تقسيم الرسالة لو تجاوزت الحد
    for i in range(0, len(full_text), MAX_MSG_LENGTH):
        bot.send_message(message.chat.id, full_text[i:i+MAX_MSG_LENGTH])
