import db_manager
from telebot import types

EMPEROR_ID = 5860391324

def register_handlers(bot):

    # 🛑 حارس البوابة الإمبراطوري (يجب أن يكون في أعلى الملف)
    @bot.message_handler(func=lambda m: db_manager.get_user(m.from_user.id).get("banned") == True)
    def stop_them(m):
        # البوت يرى الرسالة ويقرر تجاهلها تماماً (Silence)
        return

    # 💀 أمر الحظر (بالرد)
    @bot.message_handler(func=lambda m: m.text == "حظر" and m.from_user.id == EMPEROR_ID)
    def ban_process(m):
        if m.reply_to_message:
            target_id = m.reply_to_message.from_user.id
            target_name = m.reply_to_message.from_user.first_name
            
            # تحديث البيانات في الخزنة
            db_manager.update_user(target_id, {"banned": True})
            
            bot.reply_to(m, f"💀 **مـرسـوم الإقـصـاء**\n\nلقد أُغلق باب الإمبراطورية في وجه {target_name}! لن يسمع منه البوت ولن يجيبه.")
        else:
            bot.reply_to(m, "👑 **يا جلالة الإمبراطور..** أشر بالرد على من تريد إقصاءه.")

    # ✨ أمر العفو (بالرد)
    @bot.message_handler(func=lambda m: m.text == "الغاء الحظر" and m.from_user.id == EMPEROR_ID)
    def unban_process(m):
        if m.reply_to_message:
            target_id = m.reply_to_message.from_user.id
            db_manager.update_user(target_id, {"banned": False})
            bot.reply_to(m, "✨ **مـكـرمـة مـلـكـيـة**\n\nلقد رُفع الحظر بفضل جود الإمبراطور.")
