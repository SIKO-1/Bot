import os
import telebot
import importlib.util
import threading
import time

# ======================
# إعدادات أساسية
# ======================

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN غير موجود")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

COMMANDS_FOLDER = "commands"

cmd_modules = {}
game_modules = {}

# ======================
# تحميل الملفات تلقائياً حسب الاسم
# ======================

def load_modules():
    global cmd_modules, game_modules
    new_cmd = {}
    new_game = {}

    if not os.path.exists(COMMANDS_FOLDER):
        os.makedirs(COMMANDS_FOLDER)

    for filename in os.listdir(COMMANDS_FOLDER):
        if not filename.endswith(".py") or filename.startswith("__"):
            continue

        if filename.startswith("cmd_"):
            category = "cmd"
        elif filename.startswith("game_"):
            category = "game"
        else:
            continue  # تجاهل أي ملف ثاني

        module_name = filename[:-3]
        file_path = os.path.join(COMMANDS_FOLDER, filename)

        try:
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            if hasattr(module, "handle"):
                if category == "cmd":
                    new_cmd[module_name] = module
                else:
                    new_game[module_name] = module

        except Exception as e:
            print(f"خطأ في تحميل {filename}: {e}")

    cmd_modules = new_cmd
    game_modules = new_game

    print("CMD:", list(cmd_modules.keys()))
    print("GAME:", list(game_modules.keys()))

# ======================
# تحديث تلقائي (Hot Reload)
# ======================

def auto_reload():
    while True:
        load_modules()
        time.sleep(10)

threading.Thread(target=auto_reload, daemon=True).start()

# ======================
# أوامر أساسية
# ======================

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(
        message,
        "🤖 <b>بوتك شغال</b>\n"
        "• cmd_ للأوامر\n"
        "• game_ للألعاب\n"
        "كلشي يتحدث تلقائياً."
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
            print(f"خطأ داخل {module}: {e}")

# ======================
# تشغيل
# ======================

load_modules()
print("Bot is running...")
bot.infinity_polling(skip_pending=True)
