import time
import random
import db_manager

COMMANDS = ["مهمتي"]

# ======================
# إعداد المهمات المتاحة
# ======================
DAILY_TASKS = [
    {"desc": "العب لعبة النرد 🎲", "type": "play_dice"},
    {"desc": "العب لعبة الروليت 🎰", "type": "play_roulette"},
]

DAY_SECONDS = 86400  # 24 ساعة


def get_remaining_time(uid):
    user = db_manager._get_user(uid)
    last = user.get("task_taken_at", 0)
    now = time.time()

    remaining = DAY_SECONDS - (now - last)
    if remaining <= 0:
        return 0, 0

    hours = int(remaining // 3600)
    minutes = int((remaining % 3600) // 60)
    return hours, minutes


def handle(bot, message):
    uid = message.from_user.id
    text = message.text.strip()

    if text != "مهمتي":
        return

    user = db_manager._get_user(uid)
    task = user.get("daily_task", {})
    taken_at = user.get("task_taken_at", 0)

    # ===== إذا عنده مهمة حالياً =====
    if task:
        bot.reply_to(
            message,
            f"🎯 مهمتك لليوم:\n"
            f"{task.get('desc', '—')}\n\n"
            "بعد إتمامها ستحصل على صندوق الحظ النادر 🎁"
        )
        return

    # ===== تحقق من 24 ساعة =====
    if taken_at:
        hours, minutes = get_remaining_time(uid)
        if hours > 0 or minutes > 0:
            bot.reply_to(
                message,
                "⏳ لا يمكنك أخذ مهمة الآن\n\n"
                f"🕒 الوقت المتبقي:\n"
                f"• {hours} ساعة\n"
                f"• {minutes} دقيقة\n\n"
                "اصبر… الجائزة تستاهل 🎁"
            )
            return

    # ===== إعطاء مهمة جديدة =====
    new_task = random.choice(DAILY_TASKS)
    db_manager.set_daily_task(uid, new_task)

    db_manager.users.update_one(
        {"uid": uid},
        {"$set": {"task_taken_at": time.time()}}
    )

    bot.reply_to(
        message,
        f"📝 مهمتك اليومية:\n"
        f"{new_task['desc']}\n\n"
        "✨ عند إتمامها سيتم إرسال صندوق الحظ تلقائياً إلى مخزونك!"
    )


# ======================
# هذه تُستدعى من الألعاب
# ======================
def check_task_completion(bot, message, task_type):
    uid = message.from_user.id
    user = db_manager._get_user(uid)
    task = user.get("daily_task")

    if not task:
        return

    if task.get("type") != task_type:
        return

    # إكمال المهمة
    db_manager.complete_daily_task(uid)
    db_manager.add_to_inventory(uid, "🎁 صندوق الحظ النادر")

    bot.send_message(
        message.chat.id,
        "✅ تم إكمال مهمتك اليومية!\n\n"
        "🎁 تم إرسال صندوق الحظ النادر إلى مخزونك\n"
        "📦 اكتب: مخزوني لعرض المخزون"
    )
