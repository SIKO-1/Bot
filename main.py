import telebot
import os
import importlib
import sys
import time
import db_manager 
from dotenv import load_dotenv

# --- إعدادات الرقابة الملكية ---
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = 5860391324  
bot = telebot.TeleBot(TOKEN)

# متغيرات "الروح" الحقيقية
START_TIME = time.time()

print("🚀 الإمبراطورية تستعد للنهوض...")

def load_commands():
    """البحث التلقائي عن ملفات الأوامر والألعاب"""
    count = 0
    # تنظيف المسارات لضمان عدم التكرار
    for file in os.listdir("."):
        if (file.startswith("cmd_") or file.startswith("game_") or file.startswith("event_")) and file.endswith(".py"):
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

# --- 🛰️ بروتوكول رصد المجموعات المطور ---
@bot.message_handler(content_types=['new_chat_members'])
def auto_register_new_group(m):
    """تسجيل المجموعة فور دخول البوت إليها"""
    if bot.get_me().id in [user.id for user in m.new_chat_members]:
        try:
            db_manager.add_group(m.chat.id)
            bot.send_message(m.chat.id, "دخلت الإمبراطورية هذه الديار.. أعدوا العدة.")
        except: pass

# --- 🔄 أمر "تحديث" السيادي ---
@bot.message_handler(func=lambda m: m.text == "تحديث")
def restart_bot(message):
    if message.from_user.id == ADMIN_ID:
        bot.reply_to(message, "⚙️ جاري إعادة مسح ملفات الأوامر...")
        count = load_commands()
        bot.send_message(message.chat.id, f"✅ تم التحديث! الأنظمة النشطة: {count}")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # تسجيل المجموعة أو المستخدم عند ضغط start
    db_manager.add_group(message.chat.id)
    bot.reply_to(message, "🔱 كل أنظمة الإمبراطورية تعمل الآن تحت أمرك!")

# تشغيل جميع الأنظمة عند الإقلاع
loaded_count = load_commands()
print(f"📊 إجمالي الأنظمة النشطة الآن: {loaded_count}")

# --- 🔔 برقية الانبعاث ---
try:
    bot.send_message(ADMIN_ID, "مراسم الانبعاث: استعادت روح الإمبراطورية وعيها الكامل الآن.")
except: pass

# --- 🛡️ تشغيل البوت ---
if __name__ == "__main__":
    print("✅ البوت متصل الآن برتبة مشرف..")
    # تم إضافة التجاوز لضمان استمرار العمل حتى عند وقوع أخطاء بسيطة
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
