# ملف: cmd_content_control.py
from db_manager import users
import telebot

COMMANDS = ["تعطيل ملصقات", "تفعيل ملصقات", "تعطيل صور", "تفعيل صور"]

# ======================
# صلاحيات المشرف/مالك
# ======================
def is_admin(bot, message):
    try:
        member = bot.get_chat_member(message.chat.id, message.from_user.id)
        return member.status in ["administrator", "creator"]
    except:
        return False

# ======================
# إعدادات المجموعة
# ======================
def get_group_settings(chat_id):
    group = users.find_one({"chat_id": chat_id})
    if not group:
        group = {
            "chat_id": chat_id,
            "stickers_enabled": True,
            "photos_enabled": True
        }
        users.insert_one(group)
    return group

def set_group_setting(chat_id, key, value):
    users.update_one({"chat_id": chat_id}, {"$set": {key: value}})

# ======================
# تنفيذ أوامر التفعيل/التعطيل
# ======================
def handle(bot: telebot.TeleBot, message):
    chat_id = message.chat.id
    text = message.text.strip()

    if not is_admin(bot, message):
        bot.reply_to(message, "❌ فقط مالك المجموعة والمشرفين يمكنهم تعديل الإعدادات.")
        return

    group = get_group_settings(chat_id)

    if text == "تعطيل ملصقات":
        set_group_setting(chat_id, "stickers_enabled", False)
        bot.reply_to(message, "🚫 تم تعطيل الملصقات في هذه المجموعة.")
    elif text == "تفعيل ملصقات":
        set_group_setting(chat_id, "stickers_enabled", True)
        bot.reply_to(message, "✅ تم تفعيل الملصقات في هذه المجموعة.")
    elif text == "تعطيل صور":
        set_group_setting(chat_id, "photos_enabled", False)
        bot.reply_to(message, "🚫 تم تعطيل إرسال الصور في هذه المجموعة.")
    elif text == "تفعيل صور":
        set_group_setting(chat_id, "photos_enabled", True)
        bot.reply_to(message, "✅ تم تفعيل إرسال الصور في هذه المجموعة.")

# ======================
# فحص قبل الإرسال وحذف تلقائي
# ======================
def check_and_delete(bot, message):
    chat_id = message.chat.id
    settings = get_group_settings(chat_id)

    # إذا أرسل ملصق والملصقات معطلة
    if message.sticker and not settings.get("stickers_enabled", True):
        try:
            bot.delete_message(chat_id, message.message_id)
        except:
            pass
        return True

    # إذا أرسل صورة والصور معطلة
    if message.photo and not settings.get("photos_enabled", True):
        try:
            bot.delete_message(chat_id, message.message_id)
        except:
            pass
        return True

    return False
