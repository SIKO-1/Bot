import db_manager
from telebot import types

EMPEROR_ID = 5860391324

def register_handlers(bot):

    # 🛑 القاعدة الإمبراطورية: التحقق من الحظر قبل أي رد
    def check_ban(m):
        user = db_manager.get_user(m.from_user.id)
        if user and user.get("banned"):
            return True
        return False

    # 💀 أمر الحظر
    @bot.message_handler(func=lambda m: m.text == "حظر" and m.from_user.id == EMPEROR_ID)
    def ban_process(m):
        if m.reply_to_message:
            target_id = m.reply_to_message.from_user.id
            db_manager.update_user(target_id, {"banned": True})
            bot.reply_to(m, "💀 **مـرسـوم الـنـفـي**\n\nلقد سقطت عليه لعنة الإمبراطور، أُغلق البوت في وجهه!")
        else:
            bot.reply_to(m, "👑 يا مولاي، رد على رسالته لنفيه.")

    # ✨ أمر العفو
    @bot.message_handler(func=lambda m: m.text == "الغاء الحظر" and m.from_user.id == EMPEROR_ID)
    def unban_process(m):
        if m.reply_to_message:
            target_id = m.reply_to_message.from_user.id
            db_manager.update_user(target_id, {"banned": False})
            bot.reply_to(m, "✨ **مـكـرمـة مـلـكـيـة**\n\nرُفع الحظر، فليعد لخدمة العرش.")
