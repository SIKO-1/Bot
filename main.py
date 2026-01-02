import telebot
import os
import importlib
import sys

# 1. ضع التوكن الخاص بك هنا
API_TOKEN = 'YOUR_BOT_TOKEN_HERE'
bot = telebot.TeleBot(API_TOKEN)

def load_plugins():
    # تأكد أن ملفات الألعاب موجودة في مجلد اسمه plugins
    # أو غير المسار لـ "." إذا كانت الملفات بجانب الـ main.py مباشرة
    plugins_dir = "." 
    
    print("--- 🔄 جاري تحميل إمبراطورية الألعاب ---")
    
    # الحصول على قائمة الملفات وترتيبها (الألعاب أولاً لضمان الأولوية)
    files = [f for f in os.listdir(plugins_dir) if f.endswith(".py") and f != "main.py" and f != "db_manager.py"]
    
    for filename in files:
        module_name = filename[:-3]
        try:
            # استيراد الملف ديناميكياً
            spec = importlib.util.spec_from_file_location(module_name, os.path.join(plugins_dir, filename))
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
            
            # تشغيل دالة التسجيل داخل كل ملف
            if hasattr(module, 'register_handlers'):
                module.register_handlers(bot)
                print(f"✅ تم تفعيل: {module_name}")
            else:
                print(f"⚠️ الملف {module_name} لا يحتوي على دالة register_handlers")
                
        except Exception as e:
            print(f"❌ خطأ في تحميل {module_name}: {e}")

    print("--- ✨ جميع الأوامر جاهزة للعمل ---")

# تشغيل التحميل عند بدء البوت
if __name__ == "__main__":
    load_plugins()
    
    # هاندلر بسيط للتأكد أن البوت شغال
    @bot.message_handler(commands=['start', 'help'])
    def send_welcome(m):
        bot.reply_to(m, "👑 أهلاً بك في بوت الإمبراطورية، جميع الألعاب مفعلة الآن!")

    # بدء استقبال الرسائل
    print("🚀 البوت يعمل الآن على ريلوي...")
    bot.infinity_polling()
