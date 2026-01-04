import os
import telebot
import importlib.util

# ======================
# إعدادات أساسية
# ======================

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("❌ BOT_TOKEN غير موجود في Environment Variables")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

COMMANDS_FOLDER = "commands"

cmd_modules = {}
game_modules = {}

# ======================
# تحميل الملفات (مرة واحدة)
# ======================

def load_modules():
    global cmd_modules, game_modules

    if not os.path.exists(COMMANDS_FOLDER):
        os.makedirs(COMMANDS_FOLDER)

    for filename in os.listdir(COMMANDS_FOLDER):
        if not filename.endswith(".py") or filename.startswith("__"):
            continue

        if filename.startswith("cmd_"):
            target = cmd_modules
        elif filename.startswith("game_"):
            target = game_modules
        else:
            continue

        module_name = filename[:-3]
        file_path = os.path.join(COMMANDS_FOLDER, filename)

        try:
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            if hasattr(module, "handle"):
                target[module_name] = module

        except Exception as e:
            print(f"⚠️ خطأ في تحميل {filename}: {e}")

    print("CMD:", list(cmd_modules.keys()))
    print("GAME:", list(game_modules.keys()))

# ======================
# أوامر أساسية
# ======================

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(
        message,
        "🤖 <b>البوت شغال</b>\n"
        "• ملفات cmd_ = أوامر\n"
        "• ملفات game_ = ألعاب\n"
        "أعد التشغيل بعد إضافة ملفات جديدة."
    )

@bot.message_handler(commands=["help"])
def help_cmd(message):
    text = "📜 <b>الأوامر:</b>\n"

    for m in cmd_modules.values():
        if hasattr(m, "COMMAND"):
            text += f"{m.COMMAND}\n"

    text += "\n🎮 <b>الألعاب:</b>\n"

    for g in game_modules.values():
        if hasattr(g, "COMMAND"):
            text += f"{g.COMMAND}\n"

    bot.reply_to(message, text)

# ======================
# الموزّع العام
# ======================

@bot.message_handler(func=lambda message: True)
def dispatcher(message):
    for module in list(cmd_modules.values()) + list(game_modules.values()):
        try:
            module.handle(bot, message)
        except Exception as e:
            print(f"❌ خطأ داخل {module}: {e}")

# ======================
# تشغيل
# ======================

load_modules()
print("🚀 Bot is running...")
bot.infinity_polling(skip_pending=True)
