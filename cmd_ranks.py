import db_manager
from telebot import types

# الهوية الإمبراطورية الوحيدة التي تملك سلطة التعيين
EMPEROR_ID = 5860391324

def register_handlers(bot):

    # 🎖️ 1. أمر رفع ادمن (بالرد على الشخص)
    @bot.message_handler(func=lambda m: m.text == "رفع ادمن" and m.from_user.id == EMPEROR_ID)
    def promote_admin(m):
        if not m.reply_to_message:
            return bot.reply_to(m, "👑 يا إمبراطور، اختر من حاشيتك من تريد رفعه بالرد على رسالته.")

        target_id = m.reply_to_message.from_user.id
        target_name = m.reply_to_message.from_user.first_name

        # التحقق إذا كان الشخص أدمن بالفعل
        if db_manager.is_admin(target_id):
            return bot.reply_to(m, f"💡 يا مولاي، {target_name} يخدمك بالفعل كأدمن في الإمبراطورية.")

        # حفظ الرتبة في قاعدة البيانات
        db_manager.set_user_rank(target_id, "admin")
        
        text = (
            "📜 **مـرسـوم إمـبـراطـوري**\n"
            "━━━━━━━━━━━━━━\n"
            f"👤 الـعـضـو : {target_name}\n"
            "🎖️ الـرتبـة : أدمن (مساعد إمبراطوري)\n\n"
            "⚔️ تم منحه الصلاحيات لمساعدتك في إدارة الرعية."
        )
        bot.reply_to(m, text)

    # 🚫 2. أمر تنزيل ادمن (بالرد على الشخص)
    @bot.message_handler(func=lambda m: m.text == "تنزيل ادمن" and m.from_user.id == EMPEROR_ID)
    def demote_admin(m):
        if not m.reply_to_message:
            return bot.reply_to(m, "👑 يا إمبراطور، الرد مطلوب لسحب الصلاحيات.")

        target_id = m.reply_to_message.from_user.id
        target_name = m.reply_to_message.from_user.first_name

        if not db_manager.is_admin(target_id):
            return bot.reply_to(m, f"⚠️ يا مولاي، {target_name} هو مجرد عبد، ليس لديه رتبة لتنزيلها.")

        # سحب الرتبة وإعادتها لـ "عضو"
        db_manager.set_user_rank(target_id, "member")
        
        text = (
            "💢 **غـضـب إمـبـراطـوري**\n"
            "━━━━━━━━━━━━━━\n"
            f"👤 الـعـضـو : {target_name}\n"
            "❌ الـحـالـة : تم تجريده من رتبته الإدارية\n\n"
            "🐢 عاد الآن لصفوف العبيد."
        )
        bot.reply_to(m, text)

    # 🛡️ 3. حماية الأوامر من المتطفلين
    @bot.message_handler(func=lambda m: m.text in ["رفع ادمن", "تنزيل ادمن"] and m.from_user.id != EMPEROR_ID)
    def unauthorized_promotion(m):
        bot.reply_to(m, "⚠️ أنت عبد من عباد الإمبراطور، السلطة والتعيين حق حصري لجلالته فقط!")

