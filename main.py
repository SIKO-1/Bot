import telebot
import os
import importlib
import sys
from dotenv import load_dotenv

# إعدادات الرقابة الإمبراطورية
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
EMPEROR_ID = 5860391324  
bot = telebot.TeleBot(TOKEN)

def load_commands():
    """تحميل الأوامر والأحداث مع طباعة الأخطاء بوضوح"""
    count = 0
    # تحديث البحث ليشمل cmd_ و game_ و event_
    files = [f for f in os.listdir(".") if (f.startswith(("cmd_", "game_", "event_"))) and f.endswith(".py")]
    
    print(f"🔍 جاري فحص {len(files)} نظاماً إمبراطورياً...")
    
    for file in files:
        module_name = file[:-3]
        try:
            if module_name in sys.modules:
                del sys.modules[module_name]
            
            module = importlib.import_module(module_name)
            if hasattr(module, 'register_handlers'):
                module.register_handlers(bot)
                print(f"✅ تم تفعيل: {file}")
                count += 1
        except Exception as e:
            print(f"⚠️ فشل تحميل {file}: {e}")
    return count

# تشغيل الأنظمة عند البدء
print("🚀 محاولة إحياء الإمبراطورية...")
try:
    active_systems = load_commands()
    print(f"📊 الأنظمة النشطة: {active_systems}")
except Exception as e:
    print(f"❌ خطأ في التحميل: {e}")

@bot.message_handler(commands=['start'])
def start_test(m):
    bot.reply_to(m, "🔱 وصلتني رسالتك يا مولاي الإمبراطور، أنا أسمعك الآن.")

@bot.message_handler(func=lambda m: m.text == "تحديث")
def refresh_test(m):
    # السماح للإمبراطور والمشرفين فقط بالتحديث
    user_status = bot.get_chat_member(m.chat.id, m.from_user.id).status
    is_admin = user_status in ['administrator', 'creator']
    
    if m.from_user.id == EMPEROR_ID or is_admin:
        c = load_commands()
        bot.reply_to(m, f"⚙️ تم إعادة تهيئة أنظمة الإمبراطورية. العدد النشط: {c}")
    else:
        bot.reply_to(m, "ليس لديك الصلاحية لإصدار أمر التحديث.")

if __name__ == "__main__":
    print("📡 البوت يحاول الاتصال بالخوادم...")
    try:
        # إرسال إشعار للإمبراطور عند التشغيل
        bot.send_message(EMPEROR_ID, "⚠️ مراسم الانبعاث: استيقظت روح الإمبراطورية وتنتظر أوامرك.")
        bot.infinity_polling(timeout=20, long_polling_timeout=10)
    except Exception as e:
        print(f"❌ فشل الاتصال النهائي: {e}")
