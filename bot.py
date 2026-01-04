import os
import telebot
import importlib.util

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("❌ BOT_TOKEN غير موجود")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

cmd_modules = {}
game_modules = {}

def load_modules():
    global cmd_modules, game_modules

    # هنا نبحث في نفس مسار bot.py
    for filename in os.listdir(os.path.dirname(__file__)):
        if not filename.endswith(".py") or filename.startswith("__") or filename == "bot.py":
            continue

        module_name = filename[:-3]
        file_path = os.path.join(os.path.dirname(__file__), filename)

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
            print(f"⚠️ خطأ في تحميل {filename}: {e}")

    print("CMD:", list(cmd_modules.keys()))
    print("GAME:", list(game_modules.keys()))

# أوامر البوت الأساسية
@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message,
        "🤖 البوت شغال\n"
        "• أوامر: cmd_\n"
        "• ألعاب: game_\n"
        "ضع ملفات جديدة وأعد تشغيل البوت إذا أردت.")

# الموزع العام
@bot.message_handler(func=lambda m: True)
def dispatcher(message):
    for module in list(cmd_modules.values()) + list(game_modules.values()):
        try:
            module.handle(bot, message)
        except Exception as e:
            print(f"❌ خطأ في {module}: {e}")

# تشغيل
load_modules()
print("🚀 Bot is running...")
bot.infinity_polling(skip_pending=True)
