import db_manager

COMMANDS = ["ادارة_المستخدمين", "المستخدمين"]

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

        try:
            chat = bot.get_chat(uid)
            name = chat.first_name or "بدون اسم"
        except:
            name = "غير معروف"

        info = f"- {name} | ID: {uid} | 💰 {gold} | 🏦 {bank}"

        if is_banned:
            banned.append(info + " | 🚫 محظور")
        else:
            active.append(info)

    text = (
        "╔═════════════════╗\n"
        f"  أهلاً بك يا {message.from_user.first_name} في إدارة المستخدمين\n"
        "╚═════════════════╝\n\n"
        "━━━━━━━━━━━━━━━\n"
        f"👥 عدد المستخدمين الكلي: {total}\n"
        "━━━━━━━━━━━━━━━\n\n"
        "🚫 المحظورين:\n"
    )

    if banned:
        text += "\n".join(banned)
    else:
        text += "— لا يوجد —"

    text += "\n\n━━━━━━━━━━━━━━━\n\n"
    text += "✅ غير المحظورين:\n"

    if active:
        text += "\n".join(active)
    else:
        text += "— لا يوجد —"

    bot.send_message(message.chat.id, text)
