import db_manager
from telebot import types

# هوية صاحب السيادة
EMPEROR_ID = 5860391324

def register_handlers(bot):

    # 🛑 حارس البوابة الإمبراطوري
    # بما أن الملف سُمي بـ __cmd_ban سيتم تحميله قبل الألعاب والمتجر
    @bot.message_handler(func=lambda m: db_manager.get_user(m.from_user.id).get("banned") == True)
    def stop_access(m):
        # صمت ملكي مطبق.. لا رد ولا استجابة للمنبوذين
        return

    # 💀 مرسوم النفي (الحظر)
    @bot.message_handler(func=lambda m: m.text == "حظر" and m.from_user.id == EMPEROR_ID)
    def ban_command(m):
        if m.reply_to_message:
            target_id = m.reply_to_message.from_user.id
            target_name = m.reply_to_message.from_user.first_name
            
            db_manager.update_user(target_id, {"banned": True})
            bot.reply_to(m, f"💀 **مـرسـوم الإقـصـاء**\n\nلقد أُغلق باب الإمبراطورية في وجه {target_name}! لن يسمع منه البوت ولن يجيبه، فقد نُبذ وراء الأسوار.")
        else:
            bot.reply_to(m, "👑 **يا جلالة الإمبراطور..** أشر بيمينك (بالرد) على من تريد إقصاءه من رحابنا.")

    # ✨ مرسوم العفو (إلغاء الحظر)
    @bot.message_handler(func=lambda m: m.text == "عفو" and m.from_user.id == EMPEROR_ID)
    def unban_command(m):
        if m.reply_to_message:
            target_id = m.reply_to_message.from_user.id
            db_manager.update_user(target_id, {"banned": False})
            bot.reply_to(m, "✨ **مـكـرمـة مـلـكـيـة**\n\nلقد شمله عفو الإمبراطور العظيم! أُعيد العبد إلى كنف الدولة.")
        else:
            bot.reply_to(m, "👑 **يا سيدي الإمبراطور..** من هو العبد الذي نال عفوك الكريم؟ رد على رسالته.")
