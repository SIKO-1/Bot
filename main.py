import telebot
import os
import sys
import importlib.util

# محاولة تحميل dotenv
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠️ مكتبة dotenv غير مثبتة")

# 1. سحب التوكن
API_TOKEN = os.getenv('BOT_TOKEN')

# 2. إعداد البوت
bot = telebot.TeleBot(API_TOKEN, threaded=True, num_threads=20)

# --- 👑 نظام الترسيت الإمبراطوري 👑 ---
ADMIN_ID = 5860391324 

@bot.message_handler(commands=['رست', 'ترسيت'])
def restart_bot(message):
    if message.from_user.id == ADMIN_ID:
        bot.reply_to(message, "🔄 جاري إعادة التشغيل وتفريغ الذاكرة... انتظر ثوانٍ.")
        # حفظ رسالة في الذاكرة المؤقتة ليعرف البوت أنه أعاد التشغيل
        os.execv(sys.executable, ['python'] + sys.argv)
    else:
        bot.reply_to(message, "⚠️ هذا الأمر للإمبراطور فقط!")

# دالة لإرسال تأكيد عند التشغيل
def send_startup_notification():
    try:
        bot.send_message(ADMIN_ID, "✅ تم إعادة تشغيل الإمبراطورية بنجاح! البوت الآن متصل بالسحابة وجاهز للعمل.")
    except Exception as e:
        print(f"⚠️ فشل إرسال إشعار التشغيل: {e}")

# --- 📂 تحميل الألعاب والأوامر ---
def load_all_games():
    base_path = os.path.dirname(os.path.abspath(__file__))
    for filename in os.listdir(base_path):
        if (filename.startswith("game_") or filename.startswith("cmd_")) and filename.endswith(".py"):
            module_name = filename[:-3]
            try:
                spec = importlib.util.spec_from_file_location(module_name, os.path.join(base_path, filename))
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                if hasattr(module, 'register_handlers'):
                    module.register_handlers(bot)
                    print(f"✅ تم تفعيل: {module_name}")
            except Exception as e:
                print(f"⚠️ مشكلة في {module_name}: {e}")

load_all_games()

if __name__ == "__main__":
    print("╔════════════════════════════╗")
    print("   الديوان الإمبراطوري يعمل الآن   ")
    print("╚════════════════════════════╝")
    
    # إرسال إشعار للإمبراطور فور جهوزية البوت
    send_startup_notification()
    
    try:
        # التشغيل بنمط السيادة المطلقة
        bot.infinity_polling(none_stop=True, timeout=20, long_polling_timeout=10)
    except Exception as e:
        print(f"⚠️ خطأ في التوصيل: {e}")
