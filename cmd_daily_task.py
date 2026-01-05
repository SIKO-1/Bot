import db_manager

COMMANDS = ["مهمتي", "فتح الصندوق"]

def handle(bot, message):
    uid = message.from_user.id
    text = message.text.strip()

    # ========= أمر عرض المهمة =========
    if text == "مهمتي":
        task = db_manager.get_daily_task(uid)

        if not task:
            bot.reply_to(message, "❌ لا توجد مهمة حالياً.")
            return

        # لو المهمة dict
        if isinstance(task, dict):
            desc = task.get("desc", "—")
            bot.reply_to(
                message,
                f"🎯 مهمتك لليوم:\n{desc}\n\n"
                "بعد إتمامها ستحصل على صندوق الحظ النادر!"
            )
        else:
            bot.reply_to(message, f"🎯 مهمتك:\n{task}")
        return

    # ========= فتح الصندوق =========
    if text == "فتح الصندوق":
        if not db_manager.can_open_box(uid):
            bot.reply_to(message, "⏳ لم تُكمل مهمتك بعد.")
            return

        db_manager.set_box_opened(uid)
        db_manager.add_to_inventory(uid, "🎁 صندوق الحظ النادر")

        bot.reply_to(
            message,
            "✅ تم إكمال المهمة بنجاح!\n"
            "🎁 تم إرسال صندوق الحظ إلى مخزونك.\n"
            "اكتب: مخزوني لعرضه"
        )
