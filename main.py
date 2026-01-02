import telebot
import os
import importlib.util
from dotenv import load_dotenv

# تحميل المتغيرات البيئية
load_dotenv()
API_TOKEN = os.getenv('BOT_TOKEN')

# 1. إعداد البوت بنظام "تعدد المسارات" لضمان السرعة في المجموعات
# threaded=True يفتح مسار منفصل لكل مستخدم عشان ما يعلق البوت
bot = telebot.TeleBot(API_TOKEN, threaded=True, num_threads=20)

def load_all_games():
    base_path = os.path.dirname(os.path.abspath(__file__))
    print("--- 🔄 جاري فحص وتشغيل ملفات الألعاب ---")
    
    for filename in os.listdir(base_path):
        if filename.endswith(".py") and filename.startswith("game_") or filename.startswith("cmd_"):
            module_name = filename[:-3]
            try:
                spec = importlib.util.spec_from_file_location(module_name, os.path.join(base_path, filename))
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                if hasattr(module, 'register_handlers'):
                    module.register_handlers(bot)
                    print(f"✅ تم تفعيل: {module_name}")
            except Exception as e:
                print(f"⚠️ مشكلة في ملف {module_name}: {e}")

# تشغيل فحص الملفات
load_all_games()

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "👑 أهلاً بك في بوت الإمبراطورية المطور!\nالبوت يعمل الآن بنظام السرعة القصوى 🚀")

# 2. إعداد التشغيل النهائي (السطر 42 المطور)
# هذا الإعداد يمنع الانفجار ويضمن استمرار العمل بدون توقف
if __name__ == "__main__":
    print("🚀 الإمبراطورية انطلقت الآن بأقصى طاقتها...")
    bot.infinity_polling(
        timeout=90, 
        long_polling_timeout=10, 
        logger_level=5,
        skip_pending=True
    )
