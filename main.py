import telebot
import os
import importlib
import sys
from dotenv import load_dotenv
from pymongo import MongoClient

# تحميل المتغيرات
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")  # رابط MongoDB

if not TOKEN:
    raise RuntimeError("❌ BOT_TOKEN غير موجود")
if not MONGO_URI:
    raise RuntimeError("❌ MONGO_URI غير موجود")

# البوت والامبراطور
EMPEROR_ID = 5860391324
bot = telebot.TeleBot(TOKEN)

# قاعدة البيانات
mongo_client = MongoClient(MONGO_URI)
db = mongo_client["EmperorBotDB"]

# تخزين حالة الأنظمة
SYSTEM_STATUS = {}

def load_commands():
    SYSTEM_STATUS.clear()
    files = [
        f for f in os.listdir(".")
        if f.startswith(("cmd_", "game_")) and f.endswith(".py")
    ]

    for file in files:
        module_name = file[:-3]
        try:
            if module_name in sys.modules:
                del sys.modules[module_name]

            module = importlib.import_module(module_name)

            if hasattr(module, "register_handlers"):
                module.register_handlers(bot, db)
                SYSTEM_STATUS[file] = "✅ شغّال"
            else:
                SYSTEM_STATUS[file] = "⚠️ لا يوجد register_handlers"
        except Exception as e:
            SYSTEM_STATUS[file] = f"❌ فشل: {e}"

# أمر تحديث
@bot.message_handler(func=lambda m: m.text and m.text.strip().lower() == "تحديث")
def update_system(message):
    if message.from_user.id != EMPEROR_ID:
        return
    load_commands()
    report = ["📊 تقرير الأنظمة الإمبراطورية:\n"]
    for file, status in SYSTEM_STATUS.items():
        report.append(f"{status} — {file}")
    bot.send_message(message.chat.id, "\n".join(report))

# تحميل أولي
load_commands()

print("🤖 البوت يعمل وينتظر الأوامر...")
bot.infinity_polling()
