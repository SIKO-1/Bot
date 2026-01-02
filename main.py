import telebot
import os
import importlib.util

# محاولة تحميل dotenv إذا كانت موجودة، وإذا لم تكن موجودة يكمل البوت عمله
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠️ مكتبة dotenv غير مثبتة، سيتم سحب التوكن من النظام مباشرة")

# 1. سحب التوكن (تأكد أنك أضفته في Variables بموقع Railway)
API_TOKEN = os.getenv('BOT_TOKEN')

# 2. إعداد البوت مع تعدد المسارات للسرعة القصوى
bot = telebot.TeleBot(API_TOKEN, threaded=True, num_threads=20)

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
    print("🚀 البوت انطلق الآن...")
    bot.infinity_polling(timeout=90, skip_pending=True)
