import telebot
import os
import importlib
import sys
import time
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = 5860391324  
bot = telebot.TeleBot(TOKEN)

print("🚀 جاري إعادة إحياء الإمبراطورية...")

def load_systems():
    """تحميل الأنظمة بترتيب يضمن عدم التداخل"""
    count = 0
    # ترتيب الملفات: الأوامر أولاً، ثم الألعاب، ثم المستويات (الرصد العام) في النهاية
    all_files = os.listdir(".")
    ordered_files = (
        [f for f in all_files if f.startswith("event_")] +
        [f for f in all_files if f.startswith("cmd_")] +
        [f for f in all_files if f.startswith("game_")]
    )

    for file in ordered_files:
        if file.endswith(".py") and file != "main.py" and file != "db_manager.py":
            module_name = file[:-3]
            try:
                if module_name in sys.modules:
                    importlib.reload(sys.modules[module_name])
                else:
                    importlib.import_module(module_name)
                
                module = sys.modules[module_name]
                if hasattr(module, 'register_handlers'):
                    module.register_handlers(bot)
                    print(f"✅ تم تفعيل نظام: {file}")
                    count += 1
            except Exception as e:
                print(f"❌ عطل في {file}: {e}")
    return count

# تشغيل الأنظمة
active_count = load_systems()

@bot.message_handler(commands=['start'])
def welcome(m):
    bot.reply_to(m, "🔱 تحت أمرك يا صاحب السيادة، كل الأنظمة مستعدة.")

@bot.message_handler(func=lambda m: m.text == "تحديث" and m.from_user.id == ADMIN_ID)
def refresh(m):
    bot.reply_to(m, "⚙️ جاري إعادة رص الصفوف...")
    c = load_systems()
    bot.send_message(m.chat.id, f"✅ اكتمل التحديث. الأنظمة النشطة: {c}")

if __name__ == "__main__":
    print(f"📊 الإمبراطورية قائمة بـ {active_count} نظاماً.")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
