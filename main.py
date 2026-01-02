import telebot
import os
import sys  # ضروري لعملية إعادة التشغيل
import importlib.util

# محاولة تحميل dotenv
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠️ مكتبة dotenv غير مثبتة، سيتم سحب التوكن من النظام مباشرة")

# 1. سحب التوكن من إعدادات الاستضافة
API_TOKEN = os.getenv('BOT_TOKEN')

# 2. إعداد البوت مع تعدد المسارات والسرعة القصوى
bot = telebot.TeleBot(API_TOKEN, threaded=True, num_threads=20)

# --- 👑 أمر الترسيت الإمبراطوري (أولوية قصوى) 👑 ---
ADMIN_ID = 5860391324  # الأيدي الخاص بك يا إمبراطور

@bot.message_handler(commands=['رست', 'ترسيت'])
def restart_bot(message):
    if message.from_user.id == ADMIN_ID:
        bot.reply_to(message, "🔄 أبشر يا إمبراطور، جاري إعادة تشغيل النظام وتفريغ الذاكرة الآن...")
        # تنفيذ عملية الترسيت البرمجية
        os.execv(sys.executable, ['python'] + sys.argv)
    else:
        # رسالة تنبيه إذا حاول شخص آخر استخدام الأمر
        bot.reply_to(message, f"❌ هذا الأمر مخصص للإمبراطور فقط!\nمعرفك هو: {message.from_user.id}")

# --- 📂 تحميل الألعاب والأوامر من الملفات الأخرى ---
def load_all_games():
    base_path = os.path.dirname(os.path.abspath(__file__))
    for filename in os.listdir(base_path):
        # البحث عن ملفات تبدأ بـ game_ أو cmd_ وتنتهي بـ .py
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
                print(f"⚠️ مشكلة في تحميل {module_name}: {e}")

# استدعاء دالة التحميل بعد تسجيل أمر "رست"
load_all_games()

# --- 🚀 تشغيل البوت ---
if __name__ == "__main__":
    print("╔════════════════════════════╗")
    print("   الديوان الإمبراطوري يعمل الآن   ")
    print("╚════════════════════════════╝")
    try:
        # التشغيل بنمط السيادة: يتجاهل الأخطاء العابرة ولا يتوقف
        bot.infinity_polling(none_stop=True, timeout=20, long_polling_timeout=10)
    except Exception as e:
        print(f"⚠️ تنبيه سيادي: حدث خطأ غير متوقع: {e}")
