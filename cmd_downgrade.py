from telebot import TeleBot
import db_manager

def register(bot: TeleBot):

    @bot.message_handler(func=lambda m: m.text and m.text.startswith("تخفيض"))
    def downgrade_handler(message):
        from_uid = message.from_user.id
        parts = message.text.split()

        # ==========
        # تحقق من المطور
        # ==========
        if from_uid not in db_manager.DEVELOPERS:
            bot.reply_to(message, "❌ هذا الأمر للمطور فقط.")
            return

        # ==========
        # حالة الرد على شخص
        # ==========
        if message.reply_to_message:
            if len(parts) != 2:
                bot.reply_to(message, "⚠️ الصيغة:\nتخفيض <رقم_الرتبة>")
                return

            target_uid = message.reply_to_message.from_user.id
            try:
                new_rank = int(parts[1])
            except ValueError:
                bot.reply_to(message, "❌ رقم الرتبة يجب أن يكون رقمًا.")
                return

        # ==========
        # حالة استخدام ID
        # ==========
        else:
            if len(parts) != 3:
                bot.reply_to(message, "⚠️ الصيغة:\nتخفيض <ID> <رقم_الرتبة>")
                return

            try:
                target_uid = int(parts[1])
                new_rank = int(parts[2])
            except ValueError:
                bot.reply_to(message, "❌ الـ ID والرتبة يجب أن يكونوا أرقام.")
                return

        # ==========
        # تنفيذ التخفيض
        # ==========
        result = db_manager.downgrade_user_rank(
            by_uid=from_uid,
            target_uid=target_uid,
            new_rank=new_rank
        )

        if not result["ok"]:
            bot.reply_to(message, result["error"])
            return

        bot.reply_to(
            message,
            f"✅ تم التخفيض بنجاح\n"
            f"🔻 الرتبة السابقة: {result['old_rank']}\n"
            f"🔻 الرتبة الحالية: {result['new_rank']}"
                            )
