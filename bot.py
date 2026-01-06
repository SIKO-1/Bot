import os
import telebot
import importlib.util
import traceback
import db_manager

# ======================
# الإعدادات
# ======================
TOKEN = os.getenv("BOT_TOKEN")  # لازم يكون موجود في البيئة
DEV_ID = 5860391324
BOT_ENABLED = True  # متغير عالمي لتشغيل/إطفاء البوت

if not TOKEN:
    raise RuntimeError("❌ BOT_TOKEN غير موجود")

bot = telebot.TeleBot(TOKEN)  # بدون parse_mode لتجنب مشاكل HTML

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

# ======================
# أمر start
# ======================
@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(
        message,
        "🤖 البوت شغال\n"
        "• كل الأوامر موجودة في cmd_*\n"
        "• كل الألعاب موجودة في game_*\n"
        "• اكتب: تحديث"
    )

# ======================
# أمر تحديث الموديولات
# ======================
@bot.message_handler(func=lambda m: m.text=="تحديث")
def update_files(message):
    if message.from_user.id != DEV_ID:
        bot.reply_to(message,"❌ هذا الأمر للمطور فقط")
        return

    load_modules()
    report = "🔄 تم تحديث الموديولات\n\n"
    report += "✅ CMD:\n" + ("\n".join(cmd_modules.keys()) or "— لا يوجد")
    report += "\n\n🎮 GAME:\n" + ("\n".join(game_modules.keys()) or "— لا يوجد")
    if module_errors:
        report += "\n\n⚠️ أخطاء:\n"
        for f, e in module_errors.items():
            report += f"\n• {f}: {e}"

    bot.send_message(message.chat.id, report)

# ======================
# تمرير الرسائل للموديولات
# ======================
def dispatch_message(message):
    global BOT_ENABLED
    uid = message.from_user.id
    text = message.text.strip() if message.text else ""

    # ======= أوامر المطور لتشغيل/إطفاء البوت =======
    if uid == DEV_ID:
        if text == "اطفاء":
            BOT_ENABLED = False
            bot.reply_to(message, "🔴 تم إطفاء البوت بأمر الإمبراطور.")
            return
        if text == "تشغيل":
            BOT_ENABLED = True
            bot.reply_to(message, "🟢 عاد البوت للحياة بأمر الإمبراطور.")
            return

    if not BOT_ENABLED:
        return

    # ======= تمرير الرسالة للأوامر =======
    try:
        for module in cmd_modules.values():
            module.handle(bot, message)
        for module in game_modules.values():
            module.handle(bot, message)
    except Exception as e:
        traceback.print_exc()
        try:
            bot.send_message(DEV_ID, f"⚠️ خطأ من المستخدم {uid}:\n{e}")
        except:
            pass

# ======================
# Handler عام
# ======================
@bot.message_handler(func=lambda m: True)
def main_handler(message):
    dispatch_message(message)

# ======================
# تشغيل البوت
# ======================
if __name__ == "__main__":
    load_modules()
    print("🤖 البوت جاهز للعمل")
    bot.infinity_polling()
