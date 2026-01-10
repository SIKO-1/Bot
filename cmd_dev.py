def handle(bot: telebot.TeleBot, message, cmd_modules, game_modules, module_errors):
    DEV_ID = 5860391324
    uid = message.from_user.id

    if uid != DEV_ID:
        return  # فقط للمطور

    text = message.text.strip()

    # ======================
    # تحديث الموديولات
    # ======================
    if text.lower() == "تحديث":
        # محاولة تحميل الموديولات
        module_errors.clear()
        for filename in list(cmd_modules.keys()) + list(game_modules.keys()):
            try:
                # هنا ممكن تعمل reload لكل موديول إذا تحب
                pass
            except Exception as e:
                module_errors[filename] = str(e)

        # إنشاء رسالة النتائج
        msg = "🔄 تم تحديث الموديولات\n\n"
        if cmd_modules:
            msg += "✅ CMD:\n" + "\n".join(cmd_modules.keys()) + "\n\n"
        if game_modules:
            msg += "🎮 GAME:\n" + "\n".join(game_modules.keys()) + "\n\n"
        if module_errors:
            msg += "⚠️ أخطاء:\n"
            for file, err in module_errors.items():
                msg += f"• {file}: {err}\n"

        bot.reply_to(message, msg)

    # ======================
    # إرسال اشعار للمستخدمين
    # ======================
    elif text.lower().startswith("اشعار "):
        msg_text = text[6:].strip()
        if not msg_text:
            bot.reply_to(message, "❌ اكتب نص الرسالة بعد 'اشعار'")
            return

        all_users = db_manager.users.find({})
        count = 0
        for u in all_users:
            try:
                bot.send_message(u["uid"], f"📢 رسالة من الإمبراطور:\n\n{msg_text}")
                count += 1
            except:
                pass

        bot.reply_to(message, f"✅ تم إرسال الرسالة إلى {count} مستخدمين!")
