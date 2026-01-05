# ملف: cmd_users_admin.py
import db_manager

COMMANDS = ["ادارة_المستخدمين", "المستخدمين", "users_admin"]

DEV_ID = 5860391324  # ايديك كمطور

def handle(bot, message):
    if message.from_user.id != DEV_ID:
        return

    if message.text not in COMMANDS:
        return

    dev_name = message.from_user.first_name
    dev_tag = f"@{message.from_user.username}" if message.from_user.username else dev_name

    users = list(db_manager.users.find())
    total_users = len(users)

    banned_users = []
    normal_users = []

    for user in users:
        uid = user["uid"]
        gold = user.get("gold", 0)
        bank = user.get("bank", 0)
        banned = user.get("banned", False)
        username = user.get("username")
        first_name = user.get("first_name", "مستخدم")

        tag = f"@{username}" if username else first_name

        user_line = (
            f"- {tag}\n"
            f"  ID: {uid}\n"
            f"  💰 ذهب: {gold}\n"
            f"  🏦 بنك: {bank}\n"
        )

        if banned:
            banned_users.append(user_line)
        else:
            normal_users.append(user_line)

    text = ""
    text += "╔═════════════════╗\n"
    text += f"  أهلاً بك يا : {dev_tag}\n"
    text += "  في إدارة المستخدمين\n"
    text += "╚═════════════════╝\n\n"

    text += "━━━━━━━━━━━━━━━\n"
    text += f"👥 عدد المستخدمين الكلي : {total_users}\n"
    text += "━━━━━━━━━━━━━━━\n\n"

    text += "🚫 الاشخاص المحظورين :\n"
    text += "━━━━━━━━━━━━━━━\n"
    if banned_users:
        for u in banned_users:
            text += u + "\n"
    else:
        text += "- لا يوجد مستخدمين محظورين\n\n"

    text += "━━━━━━━━━━━━━━━\n"
    text += "✅ الاشخاص غير المحظورين :\n"
    text += "━━━━━━━━━━━━━━━\n"
    if normal_users:
        for u in normal_users:
            text += u + "\n"
    else:
        text += "- لا يوجد مستخدمين\n"

    bot.reply_to(message, text)
