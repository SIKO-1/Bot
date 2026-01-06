import random
import db_manager

COMMANDS = ["مهمتي"]

# ======================
# أمر: مهمتي
# ======================
def handle(bot, message):
    uid = message.from_user.id
    text = message.text.strip()

    if text != "مهمتي":
        return

    task = db_manager.get_daily_task(uid)

    # ===== لا توجد مهمة + لم يحن الوقت =====
    if task is None:
        remaining = db_manager.time_left_for_task(uid)
        if remaining:
            bot.reply_to(
                message,
                "⏳ لا يمكنك أخذ مهمة الآن\n\n"
                f"🕒 الوقت المتبقي:\n{remaining}\n\n"
                "اصبر… صندوق الحظ يحب الصابرين 🎁"
            )
        else:
            bot.reply_to(message, "❌ لا توجد مهمة حالياً.")
        return

    # ===== عرض المهمة الحالية =====
    bot.reply_to(
        message,
        f"🎯 مهمتك لليوم:\n"
        f"{task['desc']}\n\n"
        "✨ بعد إتمامها ستحصل على صندوق الحظ النادر 🎁"
    )


# ======================
# تُستدعى من الألعاب
# ======================
def check_task_completion(bot, message, mission_type):
    """
    mission_type:
    - dice
    - roulette
    - أي لعبة مستقبلية
    """

    uid = message.from_user.id

    completed = db_manager.complete_mission(uid, mission_type)

    if not completed:
        return

    db_manager.add_to_inventory(uid, "🎁 صندوق الحظ النادر")

    bot.send_message(
        message.chat.id,
        "✅ تم إكمال مهمتك اليومية بنجاح!\n\n"
        "🎁 تم إرسال صندوق الحظ النادر إلى مخزونك\n"
        "📦 اكتب: مخزوني لعرضه"
    )
