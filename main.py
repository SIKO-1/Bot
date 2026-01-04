import telebot
import os
import importlib
import sys
import time
from dotenv import load_dotenv

# --- إعدادات الرقابة الملكية ---
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = 5860391324  
bot = telebot.TeleBot(TOKEN)

# متغيرات "الروح" الحقيقية
START_TIME = time.time()
INTERNAL_ERRORS = 0

print("🚀 الإمبراطورية تستعد للنهوض...")

def load_commands():
    """البحث التلقائي عن ملفات الأوامر والألعاب"""
    count = 0
    for file in os.listdir("."):
        if (file.startswith("cmd_") or file.startswith("game_")) and file.endswith(".py"):
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
                print(f"❌ خطأ في تحميل {file}: {e}")
    return count

# تشغيل جميع الأنظمة عند الإقلاع
loaded_count = load_commands()
print(f"📊 إجمالي الأنظمة النشطة الآن: {loaded_count}")

# --- 🔔 برقية الانبعاث (تنبيه التشغيل) ---
try:
    bot.send_message(ADMIN_ID, "مراسم الانبعاث: استعادت روح الإمبراطورية وعيها الكامل الآن.")
except Exception as e:
    print(f"⚠️ تعذر إرسال برقية التشغيل: {e}")

# --- 🔄 أمر "رس" لتحديث الأنظمة ---
@bot.message_handler(func=lambda m: m.text == "رست")
def restart_bot(message):
    if message.from_user.id == ADMIN_ID:
        bot.reply_to(message, "⚙️ أبشر يا إمبراطور.. جاري إعادة مسح ملفات الأوامر والألعاب!")
        try:
            count = load_commands()
            bot.send_message(message.chat.id, f"✅ تم التحديث! الأنظمة النشطة الآن: {count}")
        except Exception as e:
            bot.reply_to(message, f"❌ حدث خطأ أثناء التحديث: {e}")
    else:
        bot.reply_to(message, "❌ هذا الأمر للإمبراطور فقط!")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🔱 كل أنظمة الإمبراطورية تعمل الآن تحت أمرك!")

# --- 🛡️ نظام مراقبة الأخطاء والاستمرارية (The Eternal Soul) ---
if __name__ == "__main__":
    print("✅ البوت متصل الآن وجاهز للاستخدام..")
    
    while True:
        try:
            bot.polling(none_stop=True, timeout=60)
        except Exception as e:
            INTERNAL_ERRORS += 1
            error_msg = f"⚠️ اضطراب في الروح: حدث خطأ داخلي.\nالسبب: {e}"
            print(error_msg)
            
            # إبلاغ الإمبراطور بالخطأ الحقيقي فور وقوعه
            try:
                bot.send_message(ADMIN_ID, error_msg)
            except:
                pass
            
            time.sleep(5)  # انتظار بسيط قبل العودة للحياة
