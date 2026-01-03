import telebot
import os
import importlib
import sys
from dotenv import load_dotenv

# تحميل الإعدادات
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = 5860391324  # ⚠️ ضع هنا الأيدي (ID) الخاص بك يا إمبراطور
bot = telebot.TeleBot(TOKEN)

print("🚀 الإمبراطورية تستعد للنهوض...")

def load_commands():
    """البحث التلقائي عن ملفات الأوامر"""
    count = 0
    for file in os.listdir("."):
        if file.startswith("cmd_") and file.endswith(".py"):
            module_name = file[:-3]
            try:
                if module_name in sys.modules:
                    importlib.reload(sys.modules[module_name])
                else:
                    importlib.import_module(module_name)
                
                module = sys.modules[module_name]
                if hasattr(module, 'register_handlers'):
                    module.register_handlers(bot)
                    print(f"✅ تم تشغيل: {file}")
                    count += 1
            except Exception as e:
                print(f"❌ خطأ في {file}: {e}")
    return count

# تشغيل الأوامر لأول مرة
load_commands()

# --- 🔄 أمر "رست" لإعادة التشغيل من التليجرام ---
@bot.message_handler(func=lambda m: m.text == "رست")
def restart_bot(message):
    if message.from_user.id == ADMIN_ID:
        bot.reply_to(message, "⚙️ أبشر يا إمبراطور.. جاري إعادة تحميل كافة الملفات وتحديث الأنظمة!")
        try:
            count = load_commands()
            bot.send_message(message.chat.id, f"✅ تم بنجاح! الأنظمة النشطة الآن: {count}")
        except Exception as e:
            bot.reply_to(message, f"❌ حدث خطأ أثناء التحديث: {e}")
    else:
        bot.reply_to(message, "❌ العب بعيد يا ادبسز.. هذا الأمر للإمبراطور فقط! 🏃‍♂️")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🔱 كل الأنظمة تعمل الآن تحت أمرك!")

if __name__ == "__main__":
    print("✅ البوت جاهز للأوامر..")
    bot.infinity_polling()
