import telebot
import os
import importlib.util
import sys

# 1. التوكن الخاص بك
API_TOKEN = 'YOUR_BOT_TOKEN_HERE'
bot = telebot.TeleBot(API_TOKEN)

def load_all_games():
    # المسار الحالي للملفات
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    print("--- 🔄 جاري مسح الإمبراطورية وتحميل الألعاب تلقائياً ---")
    
    for filename in os.listdir(base_path):
        # شروط التحميل: ملف بايثون، ليس ملف main، وليس db_manager
        if filename.endswith(".py") and filename not in ["main.py", "db_manager.py"]:
            module_name = filename[:-3]
            file_path = os.path.join(base_path, filename)
            
            try:
                # عملية الاستيراد الديناميكي
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                spec.loader.exec_module(module)
                
                # التأكد من وجود دالة التشغيل داخل ملف اللعبة
                if hasattr(module, 'register_handlers'):
                    module.register_handlers(bot)
                    print(f"✅ تم تفعيل اللعبة تلقائياً: {module_name}")
                else:
                    print(f"⚠️ الملف {module_name} موجود لكنه يفتقد لدالة register_handlers")
                    
            except Exception as e:
                print(f"❌ فشل تحميل {module_name} بسبب خطأ برمي: {e}")

# تشغيل عملية التحميل
load_all_games()

# هاندلر أساسي للتأكد من عمل البوت
@bot.message_handler(commands=['start'])
def start_cmd(m):
    bot.reply_to(m, "👑 الإمبراطورية عادت للعمل بنظام التحميل التلقائي!")

if __name__ == "__main__":
    print("🚀 البوت يعمل الآن.. أضف أي ملف لعبة وسيعمل بعد إعادة التشغيل!")
    bot.infinity_polling()
