import random
import db_manager

# أوامر الموديول
COMMANDS_TASK = ["مهمة", "مهمتي"]
COMMANDS_BOX = ["فتح الصندوق"]

# قائمة المهام اليومية
TASKS = [
    {"desc": "العب لعبة النرد 🎲", "type": "action"},
    {"desc": "العب روليت 🎰", "type": "action"},
    {"desc": "تفاعل مع البوت بـ 40 رسالة 💬", "type": "messages", "count": 40},
    {"desc": "استخدم عنصر من مخزونك 🧰", "type": "inventory", "count": 1}
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
        db_manager.set_daily_task(uid, task)  # يخزن المهمة
        bot.reply_to(
            message,
            f"🎯 مهمتك لليوم:\n{task['desc']}\nبعد إتمامها ستحصل على صندوق الحظ النادر!"
        )
        return

    # ======= فتح صندوق الحظ =======
    if text in COMMANDS_BOX:
        if not db_manager.can_open_box(uid):
            bot.reply_to(message, "⏳ ليس لديك صندوق حظ اليوم أو لم تكمل المهمة بعد.")
            return

        item = random.choice(RARE_ITEMS)
        db_manager.add_to_inventory(uid, item)
        db_manager.set_box_opened(uid)

        bot.reply_to(
            message,
            f"🎁 فتح الصندوق...\nلقد حصلت على: {item}!\nتم إضافته مباشرة إلى مخزونك."
        )
        return

    # ======= تحقق من اكتمال المهام تلقائياً =======
    task = db_manager.get_daily_task(uid)
    if task:
        if task["type"] == "messages":
            # إذا عدد الرسائل >= المطلوب
            user = db_manager._get_user(uid)
            if user.get("total_messages", 0) >= task["count"]:
                db_manager.complete_daily_task(uid)
                bot.reply_to(message, "✅ أتممت مهمتك اليومية! الصندوق النادر أصبح جاهز للفتح.")
        elif task["type"] == "inventory":
            user_inventory = db_manager.get_inventory(uid)
            if len(user_inventory) >= task["count"]:
                db_manager.complete_daily_task(uid)
                bot.reply_to(message, "✅ أتممت مهمتك اليومية! الصندوق النادر أصبح جاهز للفتح.")
