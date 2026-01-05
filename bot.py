import os
import telebot
import importlib.util
import traceback
import db_manager

TOKEN = os.getenv("BOT_TOKEN")
DEV_ID = 5860391324
if not TOKEN:
    raise RuntimeError("❌ BOT_TOKEN غير موجود")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

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
            try:
                bot.send_message(DEV_ID, f"⚠️ خطأ في تحميل {filename}:\n{e}")
            except:
                pass

    print("CMD:", list(cmd_modules.keys()))
    print("GAME:", list(game_modules.keys()))

# ======================
# تحقق الحظر قبل أي رسالة
# ======================
@bot.message_handler(func=lambda m: True)
def dispatcher(message):
    uid = message.from_user.id

    # ======= صمت عقابي للمحظورين =======
    if db_manager.is_user_banned(uid):
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except:
            pass
        # إذا تحب، ما نرسل أي رسالة → صمت كامل
        return

    # ======= تمرير الرسالة للموديولات =======
    try:
        for module in cmd_modules.values():
            module.handle(bot, message)
        for module in game_modules.values():
            module.handle(bot, message)
    except Exception as e:
        traceback.print_exc()
        try:
            bot.send_message(DEV_ID, f"⚠️ خطأ في تنفيذ رسالة {uid}:\n{e}")
        except:
            pass

# ======================
# أوامر عامة
# ======================
@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message,
        "🤖 البوت شغال\n"
        "• كل الأوامر موجودة في cmd_*\n"
        "• كل الألعاب موجودة في game_*\n"
        "• اكتب 'تحديث' لمراجعة الملفات وتشخيص الأخطاء"
    )

@bot.message_handler(func=lambda m: m.text.strip().lower() == "تحديث")
def update_files(message):
    if message.from_user.id != DEV_ID:
        bot.reply_to(message, "❌ أنت لست المطور!")
        return
    load_modules()
    report = "🔄 تم تحديث الموديولات\n\n"
    report += f"✅ CMD: {list(cmd_modules.keys())}\n"
    report += f"✅ GAME: {list(game_modules.keys())}\n"
    if module_errors:
        report += f"⚠️ أخطاء:\n" + "\n".join(f"{f}: {e}" for f, e in module_errors.items())
    bot.reply_to(message, report)

# ======================
# تشغيل البوت
# ======================
if __name__ == "__main__":
    load_modules()
    print("🤖 البوت جاهز للعمل!")
    bot.infinity_polling()
