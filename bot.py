import os
import telebot
import importlib.util
import traceback
import db_manager

# =====================
# الإعدادات
# =====================
TOKEN = os.getenv("BOT_TOKEN")  # لازم يكون موجود في البيئة
DEV_ID = 5860391324
BOT_ENABLED = True  # لتشغيل/إطفاء البوت

if not TOKEN:
    raise RuntimeError("❌ BOT_TOKEN غير موجود")

bot = telebot.TeleBot(TOKEN)  # بدون parse_mode لتجنب مشاكل HTML

cmd_modules = {}
game_modules = {}
module_errors = {}

# =====================
# تحميل الموديولات
# =====================
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
                bot.send_message(DEV_ID, f"⚠️ خطأ في تحميل الملف:\n{filename}\n{e}")
            except:
                pass

# =====================
# أوامر البوت
# =====================
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "أهلاً بك في البوت! 🤖")

@bot.message_handler(commands=["restart"])
def restart_bot(message):
    if message.from_user.id != DEV_ID:
        bot.send_message(message.chat.id, "❌ هذا الأمر للمطور فقط.")
        return
    bot.send_message(message.chat.id, "🔄 جاري إعادة تشغيل البوت...")
    os._exit(0)  # يوقف البوت ويعيد تشغيله تلقائياً على Railway/Heroku

# =====================
# التعامل مع باقي الأوامر
# =====================
@bot.message_handler(func=lambda msg: True)
def handle_commands(message):
    text = message.text
    for module_name, module in cmd_modules.items():
        try:
            module.handle(bot, message)
        except Exception as e:
            try:
                bot.send_message(DEV_ID, f"⚠️ خطأ في تنفيذ الموديول {module_name}:\n{e}")
            except:
                pass

# =====================
# بدء تحميل الموديولات
# =====================
load_modules()

# =====================
# بدء البوت
# =====================
bot.infinity_polling()
