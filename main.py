import telebot
import os
import importlib
import sys
from dotenv import load_dotenv

# تحميل المتغيرات
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("❌ BOT_TOKEN غير موجود")

EMPEROR_ID = 5860391324  # ID الإمبراطور
bot = telebot.TeleBot(TOKEN)

# حالة كل ملف / نظام
SYSTEM_STATUS = {}

def load_commands():
    """تحميل جميع الملفات الإمبراطورية وتسجيل الـ handlers"""
    SYSTEM_STATUS.clear()
    files = [
        f for f in os.listdir(".")
        if f.startswith(("cmd_", "game_", "event_")) and f.endswith(".py")
    ]

    for file in files:
        module_name = file[:-3]
        try:
            if module_name in sys.modules:
                del sys.modules[module_name]

            module = importlib.import_module(module_name)

            if hasattr(module, "register_handlers"):
                try:
                    module.register_handlers(bot)
                    SYSTEM_STATUS[file] = "✅ شغّال"
                except Exception as e:
                    SYSTEM_STATUS[file] = f"❌ فشل داخل register_handlers: {e}"
                    try:
                        bot.send_message(EMPEROR_ID, f"❌ خطأ في {file}: {e}")
                    except:
                        pass
            else:
                SYSTEM_STATUS[file] = "⚠️ لا يوجد register_handlers"

        except Exception as e:
            SYSTEM_STATUS[file] = f"❌ فشل: {e}"
            try:
                bot.send_message(EMPEROR_ID, f"❌ فشل استدعاء {file}: {e}")
            except:
                pass

# أمر تحديث باسم كلمة "تحديث" فقط
@bot.message_handler(func=lambda m: m.text and m.text.strip() == "تحديث")
def update_system(message):
    if message.from_user.id != EMPEROR_ID:
        return

    load_commands()

    report = ["📊 تقرير الأنظمة الإمبراطورية:\n"]
    for file, status in SYSTEM_STATUS.items():
        report.append(f"{status} — {file}")

    bot.send_message(
        message.chat.id,
        "\n".join(report)
    )

# تحميل أولي عند التشغيل
load_commands()

print("🤖 البوت يعمل وينتظر الأوامر...")
bot.infinity_polling()
