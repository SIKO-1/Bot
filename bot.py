import os
import telebot
import importlib.util
import traceback
import db_manager

# ======================
# الإعدادات
# ======================
TOKEN = os.getenv("BOT_TOKEN")
DEV_ID = 5860391324

if not TOKEN:
    raise RuntimeError("❌ BOT_TOKEN غير موجود")

# ❗ لا نستخدم HTML افتراضيًا حتى نتجنب الأخطاء
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
        if not filename.endswith(".py"):
            continue
        if filename.startswith("__") or filename == "bot.py":
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
                bot.send_message(
                    DEV_ID,
                    f"⚠️ خطأ في تحميل الملف:\n{filename}\n\n{e}",
                    parse_mode=None
                )
            except:
                pass

    print("CMD:", list(cmd_modules.keys()))
    print("GAME:", list(game_modules.keys()))

# ======================
# الموزّع الرئيسي (Dispatcher)
# ======================
@bot.message_handler(func=lambda m: True)
def dispatcher(message):
    uid = message.from_user.id

    # ===== صمت كامل للمحظورين =====
    if db_manager.is_user_banned(uid):
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except:
            pass
        return

    # ===== تمرير الرسائل للأوامر والألعاب =====
    try:
        for module in cmd_modules.values():
            module.handle(bot, message)

        for module in game_modules.values():
            module.handle(bot, message)

    except Exception as e:
        traceback.print_exc()
        try:
            bot.send_message(
                DEV_ID,
                f"⚠️ خطأ أثناء التنفيذ\nUID: {uid}\n\n{e}",
                parse_mode=None
            )
        except:
            pass

# ======================
# /start
# ======================
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "🤖 البوت يعمل بنجاح\n\n"
        "• الأوامر داخل ملفات cmd_*\n"
        "• الألعاب داخل ملفات game_*\n"
        "• اكتب (تحديث) لتحديث الملفات\n",
        parse_mode=None
    )

# ======================
# تحديث الملفات
# ======================
@bot.message_handler(func=lambda m: m.text and m.text.strip() != "تحديث")
def dispatcher(message):
    if message.from_user.id != DEV_ID:
        bot.send_message(message.chat.id, "❌ هذا الأمر للمطور فقط", parse_mode=None)
        return

    load_modules()

    lines = []
    lines.append("🔄 تحديث الملفات\n")

    lines.append("✅ أوامر CMD:")
    if cmd_modules:
        for m in cmd_modules:
            lines.append(f"- {m}")
    else:
        lines.append("- لا يوجد")

    lines.append("\n🎮 ألعاب GAME:")
    if game_modules:
        for g in game_modules:
            lines.append(f"- {g}")
    else:
        lines.append("- لا يوجد")

    if module_errors:
        lines.append("\n⚠️ أخطاء:")
        for f, e in module_errors.items():
            lines.append(f"- {f}: {e}")

    bot.send_message(
        message.chat.id,
        "\n".join(lines),
        parse_mode=None
    )

# ======================
# تشغيل البوت
# ======================
if __name__ == "__main__":
    load_modules()
    print("🤖 البوت جاهز للعمل")
    bot.infinity_polling(skip_pending=True)
