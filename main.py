import telebot
import os
import importlib
import pkgutil
from db_manager import get_user, update_user

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# --- كود الربط التلقائي المطور (يدعم cmd و game) ---
def load_all_modules():
    for loader, module_name, is_pkg in pkgutil.iter_modules(['.']):
        # هنا التعديل: خليناه يفحص النوعين
        if module_name.startswith('cmd_') or module_name.startswith('game_'):
            module = importlib.import_module(module_name)
            if hasattr(module, 'register_handlers'):
                module.register_handlers(bot)
                print(f"✅ تم ربط: {module_name}")

# تشغيل الربط
load_all_modules()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🚀 الإمبراطورية تعمل بنظام الملفات المنفصلة!")

print("🚀 البوت انطلق...")
bot.polling(none_stop=True)
