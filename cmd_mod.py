import db_manager
from telebot import types

# هويتك الإمبراطورية
EMPEROR_ID = 5860391324

def register_handlers(bot):

    # دالة للتحقق هل الشخص (إمبراطور أو أدمن)
    def is_authorized(user_id):
        if user_id == EMPEROR_ID:
            return True
        user_data = db_manager.get_user(user_id)
        # التحقق من الرتبة في قاعدة البيانات
        return user_data.get("rank") == "admin"

    # ⚔️ أمر الكتم (بالرد على الشخص)
    @bot.message_handler(func=lambda m: m.text == "كتم")
    def mute_member(m):
        if not is_authorized(m.from_user.id):
            bot.reply_to(m, "⚠️ أنت عبد، لا تملك سلطة الكتم!")
            return

        if not m.reply_to_message:
            return bot.reply_to(m, "👑 يا سيدي، يجب الرد على رسالة الشخص المراد كتمه.")

        target_id = m.reply_to_message.from_user.id
        target_name = m.reply_to_message.from_user.first_name
        chat_id = m.chat.id

        try:
            # استخدام خاصية التليجرام لتقييد المستخدم (آمنة جداً)
            bot.restrict_chat_member(chat_id, target_id, can_send_messages=False)
            bot.reply_to(m, f"🔇 تم إخراس {target_name} بنجاح.\nبأمر من سلطة الإمبراطورية.")
        except Exception as e:
            bot.reply_to(m, f"⚠️ لم أستطع كتمه، ربما رتبته أعلى مني في المجموعة.")

    # 🕊️ أمر إلغاء الكتم (بالرد على الشخص)
    @bot.message_handler(func=lambda m: m.text == "الغاء الكتم")
    def unmute_member(m):
        if not is_authorized(m.from_user.id):
            bot.reply_to(m, "⚠️ لا تتدخل فيما لا يعنيك!")
            return

        if not m.reply_to_message:
            return bot.reply_to(m, "👑 يا سيدي، الرد مطلوب لفك القيد.")

        target_id = m.reply_to_message.from_user.id
        target_name = m.reply_to_message.from_user.first_name
        chat_id = m.chat.id

        try:
            # إعادة كافة صلاحيات الإرسال
            bot.restrict_chat_member(chat_id, target_id, 
                can_send_messages=True, 
                can_send_media_messages=True, 
                can_send_other_messages=True, 
                can_add_web_page_previews=True)
            bot.reply_to(m, f"🔊 تم فك قيد {target_name}.\nعد للكلام بحكمة أيها العبد.")
        except Exception as e:
            bot.reply_to(m, f"⚠️ حدث خطأ: {e}")

