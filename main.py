import telebot
import os
import importlib
import pkgutil
from db_manager import get_user, update_user

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# --- كود الربط التلقائي السحري ---
def load_all_commands():
    # يبحث في المجلد الحالي عن كل الملفات
    for loader, module_name, is_pkg in pkgutil.iter_modules(['.']):
        # إذا كان اسم الملف يبدأ بـ cmd_
        if module_name.startswith('cmd_'):
            # يقوم باستيراد الملف
            module = importlib.import_module(module_name)
            # يبحث عن دالة التسجيل داخل الملف ويشغلها
            if hasattr(module, 'register_handlers'):
                module.register_handlers(bot)
                print(f"✅ تم ربط الملف تلقائياً: {module_name}")

# تشغيل الربط التلقائي
load_all_commands()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🚀 البوت يعمل بنظام الربط التلقائي والذاكرة الدائمة!")

print("🚀 البوت انطلق...")
bot.polling(none_stop=True)
