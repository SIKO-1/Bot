import os
import telebot
import importlib.util
import traceback
import db_manager
from telebot.types import ChatMember   # ⬅️ إضافة فقط

# ======================
# الإعدادات
# ======================
TOKEN = os.getenv("BOT_TOKEN")  # لازم يكون موجود في البيئة
DEV_ID = 5860391324
BOT_ENABLED = True  # متغير عالمي لتشغيل/إطفاء البوت

if not TOKEN:
    raise RuntimeError("❌ BOT_TOKEN غير موجود")

bot = telebot.TeleBot(TOKEN)  # بدون parse_mode لتجنب مشاكل HTML

cmd_modules = {}
game_modules = {}
module_errors = {}

# ======================
# تحميل الموديولات
# ======================
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

# أول تحميل
load_modules()

# ======================
# أمر start
# ======================
@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, f"👑 أهلاً بك! البوت شغال.")

# ======================
# أمر تحديث الموديولات + إشعار
# ======================
@bot.message_handler(func=lambda m: m.text is not None)
def handle_all_messages(message):
    uid = message.from_user.id
    text = message.text.strip()

    # أمر تحديث الموديولات (فقط للمطور)
    if text.lower() == "تحديث":
        if uid != DEV_ID:
            return
        load_modules()
        reply_text = "🔄 تم تحديث الموديولات\n\n"

        reply_text += "✅ CMD:\n"
        for name in cmd_modules.keys():
            reply_text += name + "\n"

        reply_text += "\n🎮 GAME:\n"
        for name in game_modules.keys():
            reply_text += name + "\n"

        if module_errors:
            reply_text += "\n⚠️ أخطاء:\n"
            for fname, err in module_errors.items():
                reply_text += f"• {fname}: {err}\n"

        bot.reply_to(message, reply_text)
        return

    # أمر اشعار (فقط للمطور)
    if text.lower().startswith("اشعار "):
        if uid != DEV_ID:
            return
        msg = text[6:].strip()
        if not msg:
            bot.reply_to(message, "❌ اكتب نص الرسالة بعد 'اشعار'")
            return

        all_users = db_manager.users.find({})
        count = 0
        for u in all_users:
            try:
                bot.send_message(u["uid"], f"📢 رسالة من الإمبراطور:\n\n{msg}")
                count += 1
            except:
                pass
        bot.reply_to(message, f"✅ تم إرسال الرسالة إلى {count} مستخدمين!")
        return

    for name, module in cmd_modules.items():
        try:
            if hasattr(module.handle, "__code__") and module.handle.__code__.co_argcount == 5:
                module.handle(bot, message, cmd_modules, game_modules, module_errors)
            else:
                module.handle(bot, message)
        except Exception as e:
            try:
                bot.send_message(DEV_ID, f"⚠️ خطأ في تنفيذ الموديول {name}:\n{e}")
            except:
                pass

    for name, module in game_modules.items():
        try:
            if hasattr(module.handle, "__code__") and module.handle.__code__.co_argcount == 5:
                module.handle(bot, message, cmd_modules, game_modules, module_errors)
            else:
                module.handle(bot, message)
        except Exception as e:
            try:
                bot.send_message(DEV_ID, f"⚠️ خطأ في تنفيذ الموديول {name}:\n{e}")
            except:
                pass

# ======================
# ⬇️⬇️ الإضافات فقط (حُرّاس الصور والملصقات)
# ======================

def is_admin(bot, chat_id, user_id):
    try:
        member = bot.get_chat_member(chat_id, user_id)
        return member.status in ["administrator", "creator"]
    except:
        return False


@bot.message_handler(content_types=["photo"])
def block_photos(message):
    chat_id = message.chat.id

    if message.chat.type == "private":
        return

    if db_manager.photos_allowed(chat_id):
        return

    if is_admin(bot, chat_id, message.from_user.id):
        return

    try:
        bot.delete_message(chat_id, message.message_id)
    except:
        pass


@bot.message_handler(content_types=["sticker"])
def block_stickers(message):
    chat_id = message.chat.id

    if message.chat.type == "private":
        return

    if db_manager.stickers_allowed(chat_id):
        return

    if is_admin(bot, chat_id, message.from_user.id):
        return

    try:
        bot.delete_message(chat_id, message.message_id)
    except:
        pass

# ======================
# تشغيل البوت
# ======================
bot.infinity_polling()
