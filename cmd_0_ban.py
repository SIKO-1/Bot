import db_manager
from telebot import types

EMPEROR_ID = 5860391324

def register_handlers(bot):

    # 🛑 حارس البوابة (Middleware)
    # هذا الفلتر يعمل على كل رسالة قبل أن تذهب لأي أمر آخر
    @bot.message_handler(func=lambda m: True, priority=1)
    def security_check(m):
        # فحص هل الشخص محظور في قاعدة البيانات
        user_data = db_manager.get_user(m.from_user.id)
        if user_data and user_data.get("banned") == True:
            # إذا كان محظوراً، نوقف المعالجة فوراً ولا نسمح للرسالة بالانتقال للأوامر الأخرى
            return
        
        # إذا لم يكن محظوراً، نسمح للرسالة بالمرور للأوامر التالية
        bot.process_new_messages([m])

    # 💀 مرسوم النفي (الحظر)
    @bot.message_handler(func=lambda m: m.text == "حظر" and m.from_user.id == EMPEROR_ID)
    def ban_action(m):
        if m.reply_to_message:
            target_id = m.reply_to_message.from_user.id
            db_manager.update_user(target_id, {"banned": True})
            bot.reply_to(m, "💀 **مـرسـوم الإقـصـاء**\n\nلقد أُغلق باب الإمبراطورية في وجهه! لن يسمع منه البوت ولن يجيبه.")
        else:
            bot.reply_to(m, "👑 يا صاحب الجلالة، أشر بالرد على من تريد إقصاءه.")

    # ✨ مرسوم العفو (إلغاء الحظر)
    @bot.message_handler(func=lambda m: m.text == "الغاء الحظر" and m.from_user.id == EMPEROR_ID)
    def unban_action(m):
        if m.reply_to_message:
            target_id = m.reply_to_message.from_user.id
            db_manager.update_user(target_id, {"banned": False})
            bot.reply_to(m, "✨ **مـكـرمـة مـلـكـيـة**\n\nلقد رُفع الحظر بفضل جود الإمبراطور.")
