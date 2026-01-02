import telebot
import os
import importlib.util

# هنا الكود سيسحب التوكن من Variables الموقع تلقائياً
# تأكد أن اسم المتغير في ريلوي هو BOT_TOKEN أو غير الاسم هنا ليطابقه
API_TOKEN = os.getenv('BOT_TOKEN') 

if not API_TOKEN:
    print("❌ خطأ: لم أجد التوكن في Variables الموقع! تأكد من تسميته BOT_TOKEN")
    exit()

bot = telebot.TeleBot(API_TOKEN)

def load_all_games():
    base_path = os.path.dirname(os.path.abspath(__file__))
    print("--- 🔄 جاري فحص ملفات الألعاب ---")
    
    for filename in os.listdir(base_path):
        if filename.endswith(".py") and filename not in ["main.py", "db_manager.py"]:
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

# تشغيل الفحص
load_all_games()

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "👑 الإمبراطورية عادت للعمل بنظام المتغيرات!")

if __name__ == "__main__":
    print("🚀 البot انطلق الآن...")
    bot.infinity_polling()
