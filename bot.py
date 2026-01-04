import os
import telebot
import importlib.util
import traceback

# ======= إعداد التوكن =======
TOKEN = os.getenv("BOT_TOKEN")
DEV_ID = 5860391324  # ايدي المطور
if not TOKEN:
    raise RuntimeError("❌ BOT_TOKEN غير موجود")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

cmd_modules = {}
game_modules = {}
module_errors = {}  # لتسجيل أي أخطاء في تحميل الملفات

# ======= تحميل الملفات تلقائيًا =======
def load_modules():
    global cmd_modules, game_modules, module_errors
    cmd_modules.clear()
    game_modules.clear()
    module_errors.clear()

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
            module_errors[filename] = str(e)
            print(f"⚠️ خطأ في تحميل {filename}: {e}")
            # إرسال تلقائي للمطور
            try:
                bot.send_message(DEV_ID, f"⚠️ خطأ في تحميل {filename}:\n{e}")
            except:
                pass

    print("CMD:", list(cmd_modules.keys()))
    print("GAME:", list(game_modules.keys()))

# ======= أوامر أساسية =======
@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message,
        "🤖 البوت شغال\n"
        "• كل الأوامر موجودة في cmd_*\n"
        "• كل الألعاب موجودة في game_*\n"
        "• اكتب 'تحديث' لمراجعة الملفات وتشخيص الأخطاء"
    )

# ======= أمر تحديث =======
@bot.message_handler(func=lambda m: m.text.strip().lower() == "تحديث")
def update_files(message):
    if message.from_user.id != DEV_ID:
        bot.reply_to(message, "❌ أنت لست المطور!")
        return

    load_modules()
    report = "🔄 تحديث الملفات:\n\n"
    report += "✅ الملفات الشغالة (CMD):\n" + "\n".join(cmd_modules.keys()) + "\n\n"
    report += "✅ الملفات الشغالة (GAME):\n" + "\n".join(game_modules.keys()) + "\n\n"

    if module_errors:
        report += "❌ الملفات التي حدثت فيها مشاكل:\n"
        for f, e in module_errors.items():
            report += f"{f} → {e}\n"
    else:
        report += "🎉 لا توجد مشاكل في الملفات"

    bot.send_message(DEV_ID, report)
    bot.reply_to(message, "🔄 تم تحديث الملفات. تقرير أرسل لك كمطور!")

# ======= موزع الرسائل =======
@bot.message_handler(func=lambda m: True)
def dispatcher(message):
    for module in list(cmd_modules.values()) + list(game_modules.values()):
        try:
            module.handle(bot, message)
        except Exception as e:
            err_msg = f"❌ خطأ في {module.__name__}:\n{e}\n{traceback.format_exc()}"
            print(err_msg)
            # إرسال تلقائي للمطور
            try:
                bot.send_message(DEV_ID, err_msg)
            except:
                pass

# ======= تشغيل البوت =======
load_modules()
print("🚀 Bot is running...")
bot.infinity_polling(skip_pending=True)
