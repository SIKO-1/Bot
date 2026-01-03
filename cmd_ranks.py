import db_manager
from telebot import types

# الهوية الإمبراطورية
EMPEROR_ID = 5860391324

def register_handlers(bot):

    @bot.message_handler(func=lambda m: m.text and m.text.strip() == "رفع ادمن")
    def promote_process(m):
        if m.from_user.id != EMPEROR_ID:
            bot.reply_to(m, "⚠️ أنت عبد من عباد الإمبراطور، السلطة والتعيين حق حصري لجلالته فقط!")
            return

        if not m.reply_to_message:
            bot.reply_to(m, "👑 يا إمبراطور، يجب الرد على رسالة الشخص لرفعه.")
            return

        target_id = m.reply_to_message.from_user.id
        target_name = m.reply_to_message.from_user.first_name

        try:
            # التعديل هنا: نرسل ID المستخدم، ثم قاموساً بالبيانات الجديدة (argumentين فقط)
            # الرتبة يتم تخزينها داخل الـ Volume الخاص بالمستخدم
            db_manager.update_user(target_id, {"rank": "admin"})
            
            text = (
                "📜 **مـرسـوم إمـبـراطـوري**\n"
                "━━━━━━━━━━━━━━\n"
                f"👤 الـعـضـو : {target_name}\n"
                "🎖️ الـرتبـة : أدمن (مساعد إمبراطوري)\n\n"
                "⚔️ تم منحه الصلاحيات بنجاح."
            )
            bot.reply_to(m, text)
        except Exception as e:
            bot.reply_to(m, f"⚠️ حدث خطأ تقني يا مولاي: {e}")

    @bot.message_handler(func=lambda m: m.text and m.text.strip() == "تنزيل ادمن")
    def demote_process(m):
        if m.from_user.id != EMPEROR_ID:
            bot.reply_to(m, "⚠️ لا تتدخل في شؤون العرش!")
            return

        if not m.reply_to_message:
            bot.reply_to(m, "👑 يا إمبراطور، الرد مطلوب لسحب الصلاحيات.")
            return

        target_id = m.reply_to_message.from_user.id
        target_name = m.reply_to_message.from_user.first_name

        try:
            # إعادة الرتبة إلى عضو عادي
            db_manager.update_user(target_id, {"rank": "member"})

            bot.reply_to(m, f"💢 تم تجريد {target_name} من رتبته الإدارية وعاد لصفوف العبيد.")
        except Exception as e:
            bot.reply_to(m, f"⚠️ خطأ: {e}")
