import telebot
import os
import importlib
import sys
from dotenv import load_dotenv

# تحميل العرش الرقمي
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
EMPEROR_ID = 5860391324  # هويتك السيادية
bot = telebot.TeleBot(TOKEN)

def load_empire_systems():
    """استدعاء كافة الأنظمة المسجلة في الديوان"""
    count = 0
    # البحث عن ملفات الأوامر والألعاب والأحداث
    files = [f for f in os.listdir(".") if f.startswith(("cmd_", "game_", "event_")) and f.endswith(".py")]
    
    for file in files:
        module_name = file[:-3]
        try:
            if module_name in sys.modules:
                importlib.reload(sys.modules[module_name])
            else:
                importlib.import_module(module_name)
            
            module = sys.modules[module_name]
            if hasattr(module, "register_handlers"):
                module.register_handlers(bot)
                count += 1
                print(f"✅ تم تفعيل نظام: {file}")
        except Exception as e:
            print(f"⚠️ فشل في إقلاع {file}: {e}")
    return count

@bot.message_handler(commands=['start'])
def start_emperor(m):
    bot.reply_to(m, "🔱 الإمبراطورية في خدمتكم، كل الأنظمة مفعلة الآن.")

@bot.message_handler(func=lambda m: m.text == "تحديث" and m.from_user.id == EMPEROR_ID)
def refresh_systems(m):
    c = load_empire_systems()
    bot.reply_to(m, f"⚙️ تم إعادة مزامنة الأنظمة. عدد الأنظمة النشطة: {c}")

if __name__ == "__main__":
    load_empire_systems()
    print("📡 البوت متصل بالخادم الإمبراطوري...")
    try:
        bot.infinity_polling(timeout=20)
    except Exception as e:
        print(f"❌ خطأ اتصال: {e}")
