import os
import telebot
import importlib.util
import traceback
import db_manager
import sys

# ======================
# الإعدادات
# ======================
TOKEN = os.getenv("BOT_TOKEN")  # لازم يكون موجود في البيئة
DEV_ID = 5860391324
BOT_ENABLED = True  # متغير عالمي لتشغيل/إطفاء البوت

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
                elif filename.startswith("game_"):
                    game_modules[module_name] = module

        except Exception as e:
            module_errors[filename] = str(e)
            try:
                bot.send_message(DEV_ID, f"⚠️ خطأ في تحميل الملف:\n{filename}\n{e}")
            except:
                pass

# تحميل الموديولات أول مرة
load_modules()

# ======================
# إعادة تحميل الموديولات (Restart)
# ======================
def restart_bot(chat_id=None):
    try:
        load_modules()
        if chat_id:
            bot.send_message(chat_id, "♻️ تم إعادة تشغيل النظام بنجاح!")
    except Exception as e:
        bot.send_message(DEV_ID, f"❌ خطأ أثناء إعادة التشغيل:\n{e}")

# ======================
# أمر start
# ======================
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "👋 هلا، البوت شغال!")

# ======================
# أمر رست
# ======================
@bot.message_handler(commands=["رست"])
def restart_cmd(message):
    if message.from_user.id != DEV_ID:
        bot.reply_to(message, "❌ هذا الأمر للمطور فقط")
        return
    restart_bot(message.chat.id)

# ======================
# تفعيل أوامر cmd
# ======================
for module in list(cmd_modules.values()):
    try:
        if hasattr(module, "register_marriage"):
            module.register_marriage(bot)
        else:
            module.handle(bot, None)  # لو عنده handle عام
    except Exception as e:
        bot.send_message(DEV_ID, f"⚠️ خطأ عند تسجيل الموديول:\n{module}\n{e}")

# ======================
# بدء الاستماع
# ======================
bot.infinity_polling()
