import telebot
import os
import sys  # أضفنا مكتبة النظام للتحكم في إعادة التشغيل
import importlib.util

# محاولة تحميل dotenv إذا كانت موجودة
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠️ مكتبة dotenv غير مثبتة، سيتم سحب التوكن من النظام مباشرة")

# 1. سحب التوكن
API_TOKEN = os.getenv('BOT_TOKEN')

# 2. إعداد البوت مع تعدد المسارات للسرعة القصوى
bot = telebot.TeleBot(API_TOKEN, threaded=True, num_threads=20)

# --- 👑 أمر الترسيت (للمطور فقط) 👑 ---
ADMIN_ID = 5860391324  # الأيدي الخاص بك يا إمبراطور

@bot.message_handler(commands=['رست', 'ترسيت'])
def restart_bot(message):
    if message.from_user.id == ADMIN_ID:
        bot.reply_to(message, "🔄 أبشر يا إمبراطور، جاري إعادة تشغيل النظام وتفريغ الذاكرة...")
        # هذا السطر يغلق البوت ويفتحه من جديد فوراً
        os.execv(sys.executable, ['python'] + sys.argv)
    else:
        bot.reply_to(message, "⚠️ هذا الأمر للإمبراطور فقط، لا تتدخل في شؤون الحكم!")

# --- تحميل الألعاب والأوامر ---
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
    print("╔═════════════════╗")
    print("   الديوان الإمبراطوري يعمل الآن")
    print("╚═════════════════╝")
    try:
        # التشغيل بنمط السيادة المطلقة مع تحسين أداء الانتظار (Timeout)
        bot.infinity_polling(none_stop=True, timeout=20, long_polling_timeout=10)
    except Exception as e:
        print(f"⚠️ تنبيه سيادي: حدث خطأ في النظام: {e}")
