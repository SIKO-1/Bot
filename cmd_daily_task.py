import random
import db_manager

# أوامر الموديول
COMMANDS_TASK = ["مهمة", "مهمتي"]
COMMANDS_BOX = ["فتح الصندوق"]

# قائمة المهام اليومية
TASKS = [
    "العب لعبة النرد 🎲",
    "العب روليت 🎰",
    "تفاعل مع البوت بـ 40 رسالة 💬",
    "استخدم عنصر من مخزونك 🧰"
]

# العناصر النادرة التي يمكن الحصول عليها من الصندوق
RARE_ITEMS = [
    "سيف الإمبراطور 🔱",
    "درع الحماية الأسطوري 🛡️",
    "خاتم التفاعل 💍",
    "عملة الإمبراطور 💰",
    "كتاب الحكمة 📜",
    "خوذة الحكيم 🪖",
    "بلورة الزمن ⏳"
]

def handle(bot, message):
    uid = message.from_user.id
    text = message.text.strip()

    # ======= مهمات يومية =======
    if text in COMMANDS_TASK:
        task = random.choice(TASKS)
        db_manager.set_daily_task(uid, task)
        bot.reply_to(
            message,
            f"🎯 مهمتك لليوم:\n{task}\nبعد إتمامها ستحصل على صندوق الحظ النادر!"
        )

    # ======= فتح صندوق الحظ =======
    elif text in COMMANDS_BOX:
        if not db_manager.can_open_box(uid):
            bot.reply_to(message, "⏳ ليس لديك صندوق حظ اليوم أو لم تكمل المهمة بعد.")
            return

        item = random.choice(RARE_ITEMS)
        db_manager.add_to_inventory(uid, item)  # يروح مباشرة للمخزون
        db_manager.set_box_opened(uid)

        bot.reply_to(
            message,
            f"🎁 فتح الصندوق...\nلقد حصلت على: {item}!\nتم إضافته مباشرة إلى مخزونك."
        )
