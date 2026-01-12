# cmd_users_admin.py
from db_manager import users_col

# ======= إعداد المطورين =======
DEV_IDS = [5860391324, 7076215547, 7855813063]  # أضف كل المطورين هنا
COMMANDS = ["ادارة_المستخدمين", "المستخدمين"]
MAX_MSG_LENGTH = 4000  # الحد الأقصى لرسائل Telegram

async def handle(bot, message):
    uid = message.from_user.id
    text = message.text.strip()

    if text not in COMMANDS:
        return

    if uid not in DEV_IDS:
        await bot.send_message(message.chat.id, "❌ هذا الأمر للمطورين فقط")
        return

    users = await users_col.find({}).to_list(length=None)
    total = len(users)

    banned = []
    active = []

    for user in users:
        user_id = user["uid"]
        gold = user.get("gold", 0)
        bank = user.get("bank", 0)
        is_banned = user.get("banned", False)
        name = user.get("name", f"مستخدم {user_id}")

        info = f"- {name} | ID: {user_id} | 💰 {gold} | 🏦 {bank}"
        if is_banned:
            banned.append(info + " | 🚫 محظور")
        else:
            active.append(info)

    text_header = f"""╔═════════════════╗
  أهلاً بك يا {message.from_user.first_name} في إدارة المستخدمين
╚═════════════════╝

👥 عدد المستخدمين الكلي: {total}

🚫 المحظورين:
"""

    text_banned = "\n".join(banned)
    text_active = "\n\n✅ غير المحظورين:\n" + "\n".join(active)

    full_text = text_header + text_banned + text_active

    # تقسيم الرسالة لو تجاوزت الحد
    for i in range(0, len(full_text), MAX_MSG_LENGTH):
        await bot.send_message(message.chat.id, full_text[i:i+MAX_MSG_LENGTH])
