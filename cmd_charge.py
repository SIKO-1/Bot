import db_manager

# 🆔 ايدي المطور
DEVELOPER_ID = 5860391324

COMMANDS = ["شحن"]

def handle(bot, message):
    if not message.text:
        return

    parts = message.text.split()

    if parts[0] not in COMMANDS:
        return

    # 🔒 حماية: المطور فقط
    if message.from_user.id != DEVELOPER_ID:
        bot.reply_to(message, "❌ هذا الأمر مخصص للمطور فقط")
        return

    # =====================
    # حالة الرد على شخص
    # =====================
    if message.reply_to_message:
        if len(parts) != 2:
            bot.reply_to(message, "⚠️ الصيغة:\nشحن <الكمية>")
            return

        try:
            amount = int(parts[1])
        except ValueError:
            bot.reply_to(message, "❌ الكمية لازم تكون رقم")
            return

        if amount <= 0:
            bot.reply_to(message, "❌ الكمية لازم تكون أكبر من صفر")
            return

        target = message.reply_to_message.from_user
        new_gold = db_manager.update_user_gold(target.id, amount)

        bot.send_message(
            message.chat.id,
            f"✅ تم شحن المستخدم بنجاح\n\n"
            f"👤 الاسم: {target.first_name}\n"
            f"🆔 ID: {target.id}\n"
            f"💰 المبلغ: +{amount}\n"
            f"✨ الرصيد الحالي: {new_gold}"
        )
        return

    # =====================
    # حالة الإيدي
    # =====================
    if len(parts) != 3:
        bot.reply_to(
            message,
            "⚠️ الصيغة الصحيحة:\n"
            "شحن <ID> <الكمية>\n"
            "أو رد على الشخص واكتب:\n"
            "شحن <الكمية>"
        )
        return

    try:
        target_id = int(parts[1])
        amount = int(parts[2])
    except ValueError:
        bot.reply_to(message, "❌ ID والكمية لازم يكونوا أرقام")
        return

    if amount <= 0:
        bot.reply_to(message, "❌ الكمية لازم تكون أكبر من صفر")
        return

    new_gold = db_manager.update_user_gold(target_id, amount)

    bot.send_message(
        message.chat.id,
        f"✅ تم شحن الحساب بنجاح\n\n"
        f"🆔 ID: {target_id}\n"
        f"💰 المبلغ: +{amount}\n"
        f"✨ الرصيد الحالي: {new_gold}"
    )
