import telebot
import os
import importlib.util

# --- إعداد التوكن المباشر لضمان عدم الانفجار ---
# ضع التوكن الخاص بك هنا مباشرة بين القوسين إذا استمر الخطأ
API_TOKEN = os.getenv('BOT_TOKEN') or "حط_التوكن_هنا_إذا_مانفع_السحب_التلقائي"

# إعداد البوت مع دعم تعدد المسارات (السرعة القصوى)
bot = telebot.TeleBot(API_TOKEN, threaded=True, num_threads=20)

def load_all_games():
    base_path = os.path.dirname(os.path.abspath(__file__))
    print("--- 🔄 جاري تشغيل الأنظمة ---")
    
    for filename in os.listdir(base_path):
        if (filename.startswith("game_") or filename.startswith("cmd_")) and filename.endswith(".py"):
            module_name = filename[:-3]
            try:
                spec = importlib.util.spec_from_file_location(module_name, os.path.join(base_path, filename))
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                if hasattr(module, 'register_handlers'):
                    module.register_handlers(bot)
                    print(f"✅ فعال: {module_name}")
            except Exception as e:
                print(f"⚠️ خطأ في {module_name}: {e}")

load_all_games()

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "🚀 البوت يعمل الآن بأقصى سرعة!")

if __name__ == "__main__":
    print("🚀 انطلق الإمبراطور...")
    try:
        bot.infinity_polling(timeout=90, skip_pending=True)
    except Exception as e:
        print(f"❌ خطأ في التشغيل: {e}")
