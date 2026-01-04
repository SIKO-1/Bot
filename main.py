import telebot
import os
import importlib
import sys
from dotenv import load_dotenv

# تحميل المتغيرات السيادية
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
EMPEROR_ID = 5860391324

if not TOKEN:
    print("❌ خطأ: BOT_TOKEN غير متاح في الخزينة")
    sys.exit()

bot = telebot.TeleBot(TOKEN)
SYSTEM_STATUS = {}

def load_commands():
    SYSTEM_STATUS.clear()
    # شمولية البحث لتشمل كافة الأنظمة
    files = [f for f in os.listdir(".") if f.startswith(("cmd_", "game_", "event_")) and f.endswith(".py")]

    for file in files:
        module_name = file[:-3]
        try:
            if module_name in sys.modules:
                importlib.reload(sys.modules[module_name])
            else:
                importlib.import_module(module_name)

            module = sys.modules[module_name]
            # التسجيل بمتغير واحد (bot) لضمان التوافق الشامل
            if hasattr(module, "register_handlers"):
                module.register_handlers(bot)
                SYSTEM_STATUS[file] = "✅ نشط"
            else:
                SYSTEM_STATUS[file] = "⚠️ مفقود"
        except Exception as e:
            SYSTEM_STATUS[file] = f"❌ عطل: {e}"

@bot.message_handler(func=lambda m: m.text == "تحديث" and m.from_user.id == EMPEROR_ID)
def update_system(message):
    load_commands()
    report = ["📊 تقرير جرد الأنظمة:\n"]
    for file, status in SYSTEM_STATUS.items():
        report.append(f"{file} | {status}")
    bot.reply_to(message, "\n".join(report))

# مراسم الإقلاع
if __name__ == "__main__":
    load_commands()
    print("🔱 الإمبراطورية مستعدة لتلقي الأوامر...")
    try:
        bot.send_message(EMPEROR_ID, "⚠️ تم إعادة تفعيل كافة الأنظمة بنجاح.")
        bot.infinity_polling(timeout=20)
    except Exception as e:
        print(f"❌ فشل في الاتصال السحابي: {e}")
