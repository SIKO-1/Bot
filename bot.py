import os
import telebot
import importlib.util
import traceback
import db_manager

======================

الإعدادات

======================

TOKEN = os.getenv("BOT_TOKEN")  # لازم يكون موجود في البيئة
DEV_ID = 5860391324
BOT_ENABLED = True  # متغير عالمي لتشغيل/إطفاء البوت

if not TOKEN:
raise RuntimeError("❌ BOT_TOKEN غير موجود")

bot = telebot.TeleBot(TOKEN)  # بدون parse_mode لتجنب مشاكل HTML

cmd_modules = {}
game_modules = {}
module_errors = {}

======================

تحميل الموديولات

======================

def load_modules():
global cmd_modules, game_modules, module_errors

cmd_modules.clear()  
game_modules.clear()  
module_errors.clear()  

base_path = os.path.dirname(__file__)  

for filename in os.listdir(base_path):  
    if not filename.endswith(".py") or filename.startswith("__") or filename=="bot.py":  
        continue  
    module_name = filename[:-3]  
    file_path = os.path.join(base_path, filename)  

    try:  
        spec = importlib.util.spec_from_file_location(module_name, file_path)  
        module = importlib.util.module_from_spec(spec)  
        spec.loader.exec_module(module)  

        if hasattr(module, "handle"):  
            if filename.startswith("cmd_"):  
                cmd_modules[module_name] = module  
            elif filename.startswith("game_"):  
                game_modules[module_name] = module  

    except Exception as e:  
        module_errors[filename] = str(e)  
        try:  
            bot.send_message(DEV_ID, f"⚠️ خطأ في تحميل الملف:\n{filename}\n{e}")  
        except:  
            pass

======================

أمر start

======================

@bot.message_handler(commands=["start"])
def start(message):
    
