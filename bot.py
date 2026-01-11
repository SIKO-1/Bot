import os
import sys
import telebot
import importlib.util
import db_manager

# ======================
# الإعدادات
# ======================
TOKEN = os.getenv("BOT_TOKEN")
DEV_ID = 5860391324

if not TOKEN:
    raise RuntimeError("❌ BOT_TOKEN غير موجود")

bot = telebot.TeleBot(TOKEN)

cmd_modules = {}
game_modules = {}
module_errors = {}

# ======================
# تحميل الموديولات
# ======================
def load_modules():
    global cmd_modules, game_modules, module_errors
    cmd_modules.clear()
    game_modules.clear()
    module_errors.clear()

    base_path = os.path.dirname(__file__)
    for filename in os.listdir(base_path):
        if not filename.endswith(".py") or filename.startswith("__") or filename == "bot.py":
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
                elif filename.startswith("game_"):
                    game_modules[module_name] = module

        except Exception as e:
            module_errors[filename] = str(e)
            try:
                bot.send_message(DEV_ID, f"⚠️ خطأ تحميل:\n{filename}\n{e}")
            except:
                pass

load_modules()

# ======================
# أدوات مساعدة
# ======================
def is_admin(chat_id, user_id):
    try:
        member = bot.get_chat_member(chat_id, user_id)
        return member.status in ["administrator", "creator"]
    except:
        return False

# ======================
# start
# ======================
@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "👑 البوت شغال.")

# ======================
# الرسائل النصية
# ======================
@bot.message_handler(func=lambda m: m.text is not None)
def handle_text(message):
    uid = message.from_user.id
    chat_id = message.chat.id
    text = message.text.strip()

    # تحديث الموديولات
    if text.lower() == "تحديث" and uid == DEV_ID:
        load_modules()
        reply = "🔄 تم تحديث الموديولات\n\n✅ CMD:\n"
        for m in cmd_modules:
            reply += m + "\n"
        reply += "\n🎮 GAME:\n"
        for g in game_modules:
            reply += g + "\n"
        if module_errors:
            reply += "\n⚠️ أخطاء:\n"
            for fname, err in module_errors.items():
                reply += f"• {fname}: {err}\n"
        bot.reply_to(message, reply)
        return

    # ريست البوت
    if text in ["ريست", "إعادة تشغيل"] and uid == DEV_ID:
        bot.reply_to(message, "♻️ يتم إعادة تشغيل البوت...")
        os.execv(sys.executable, [sys.executable] + sys.argv)

    # تمرير الرسائل لبقية الموديولات
    for module in cmd_modules.values():
        try:
            module.handle(bot, message)
        except Exception as e:
            try:
                bot.send_message(DEV_ID, f"⚠️ خطأ في تنفيذ الموديول {module}:\n{e}")
            except:
                pass

    for module in game_modules.values():
        try:
            module.handle(bot, message)
        except Exception as e:
            try:
                bot.send_message(DEV_ID, f"⚠️ خطأ في تنفيذ الموديول {module}:\n{e}")
            except:
                pass

# ======================
# الرسائل الخاصة للموديولات
# ======================
@bot.message_handler(func=lambda m: m.chat.type == "private")
def handle_private_messages(m):
    for module in cmd_modules.values():
        if hasattr(module, "handle_private"):
            try:
                module.handle_private(bot, m)
            except:
                pass

# ======================
# أزرار Inline للموديولات
# ======================
@bot.callback_query_handler(func=lambda c: True)
def handle_callbacks(c):
    for module in cmd_modules.values():
        if hasattr(module, "handle_callback"):
            try:
                module.handle_callback(bot, c)
            except:
                pass

# ======================
# تشغيل البوت
# ======================
bot.infinity_polling()
