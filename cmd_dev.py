import telebot
import os
import importlib.util

COMMANDS = ["تحديث", "اشعار"]

def handle(bot: telebot.TeleBot, message, cmd_modules, game_modules, module_errors):
    DEV_ID = 5860391324
    uid = message.from_user.id

    if uid != DEV_ID:
        return  # فقط للمطور

    text = message.text.strip()

    # ======================================
    # أمر تحديث الموديولات
    # ======================================
    if text.lower() == "تحديث":
        base_path = os.path.dirname(__file__)
        cmd_modules.clear()
        game_modules.clear()
        module_errors.clear()

        loaded_cmds = []
        loaded_games = []

        for filename in os.listdir(base_path):
            if not filename.endswith(".py") or filename.startswith("__") or filename=="bot.py":
                continue
            module_name = filename[:-3]
            file_path = os.path.join(base_path, filename)

            try:
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                if hasattr(module, "handle"):
                    if filename.startswith("cmd_"):
                        cmd_modules[module_name] = module
                        loaded_cmds.append(module_name)
                    elif filename.startswith("game_"):
                        game_modules[module_name] = module
                        loaded_games.append(module_name)

            except Exception as e:
                module_errors[filename] = str(e)

        msg_lines = ["🔄 تم تحديث الموديولات\n"]
        if loaded_cmds:
            msg_lines.append("✅ CMD:")
            for m in loaded_cmds:
                msg_lines.append(m)
        if loaded_games:
            msg_lines.append("\n🎮 GAME:")
            for g in loaded_games:
                msg_lines.append(g)
        if module_errors:
            msg_lines.append("\n⚠️ أخطاء:")
            for f, err in module_errors.items():
                msg_lines.append(f"• {f}: {err}")

        bot.reply_to(message, "\n".join(msg_lines))

    # ======================================
    # أمر إرسال رسالة جماعية
    # ======================================
    elif text.lower().startswith("اشعار "):
        msg = text[6:].strip()
        if not msg:
            bot.reply_to(message, "❌ اكتب نص الرسالة بعد 'اشعار'")
            return

        all_users = cmd_modules.get("db_manager").users.find({}) if "db_manager" in cmd_modules else []
        count = 0
        for u in all_users:
            try:
                bot.send_message(u["uid"], f"📢 رسالة من الإمبراطور:\n\n{msg}")
                count += 1
            except:
                pass

        bot.reply_to(message, f"✅ تم إرسال الرسالة إلى {count} مستخدمين!")
