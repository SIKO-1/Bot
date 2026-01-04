import telebot
import os
import importlib
import sys
from dotenv import load_dotenv

# إعدادات الرقابة
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = 5860391324  
bot = telebot.TeleBot(TOKEN)

def load_commands():
    """تحميل الأوامر مع طباعة الأخطاء بوضوح"""
    count = 0
    # الحصول على قائمة الملفات التي تبدأ بـ cmd_ أو game_
    files = [f for f in os.listdir(".") if (f.startswith("cmd_") or f.startswith("game_")) and f.endswith(".py")]
    
    print(f"🔍 جاري فحص {len(files)} نظاماً...")
    
    for file in files:
        module_name = file[:-3]
        try:
            # مسح الموديل من الذاكرة لإعادة تحميله نظيفاً
            if module_name in sys.modules:
                del sys.modules[module_name]
            
            module = importlib.import_module(module_name)
            if hasattr(module, 'register_handlers'):
                module.register_handlers(bot)
                print(f"✅ تم تفعيل: {file}")
                count += 1
        except Exception as e:
            print(f"⚠️ فشل تحميل {file} بسبب خطأ في الكود الداخلي: {e}")
    return count

# تشغيل الأنظمة
print("🚀 محاولة إحياء الإمبراطورية...")
try:
    active_systems = load_commands()
    print(f"📊 الأنظمة النشطة: {active_systems}")
except Exception as e:
    print(f"❌ خطأ كارثي أثناء التحميل: {e}")

@bot.message_handler(commands=['start'])
def start_test(m):
    bot.reply_to(m, "🔱 وصلتني رسالتك يا مولاي، أنا أسمعك الآن.")

@bot.message_handler(func=lambda m: m.text == "تحديث" and m.from_user.id == ADMIN_ID)
def refresh_test(m):
    c = load_commands()
    bot.reply_to(m, f"⚙️ تم إعادة تهيئة الأنظمة. العدد: {c}")

if __name__ == "__main__":
    print("📡 البوت يحاول الاتصال بالخوادم الآن...")
    try:
        bot.send_message(ADMIN_ID, "مراسم الانبعاث: استيقظت روح الإمبراطورية.")
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except Exception as e:
        print(f"❌ فشل الاتصال النهائي: {e}")
