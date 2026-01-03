import db_manager
from telebot import types

EMPEROR_ID = 5860391324

def register_handlers(bot):

    # 🛑 الوظيفة الأهم: حارس البوابة الإمبراطوري
    # قمنا بإضافة 'update_types' لضمان مراقبة كل شيء
    @bot.message_handler(func=lambda m: db_manager.is_user_muted(m.from_user.id), priority=100)
    def block_muted_users(m):
        # هنا البوت يرى الرسالة ولكن "يبلعها" ولا يرد عليها أبداً
        return

    # ⚔️ أمر الكتم (بالرد على الشخص)
    @bot.message_handler(func=lambda m: m.text == "كتم")
    def mute_action(m):
        if m.from_user.id != EMPEROR_ID:
            bot.reply_to(m, "⚠️ أنت عبد من عباد الإمبراطور، لا تتجرأ وتقول ذلك ثانية!")
            return

        if m.reply_to_message:
            target_id = m.reply_to_message.from_user.id
            target_name = m.reply_to_message.from_user.first_name
            
            # حفظ في الخزنة (db_manager)
            db_manager.mute_user(target_id, target_name)
            bot.reply_to(m, f"⚔️ تم إخراس {target_name} نهائياً. لن يستجيب له البوت بعد الآن.")
        else:
            bot.reply_to(m, "👑 يا إمبراطور، يجب الرد على رسالة العبد المراد كتمه.")

    # 🕊️ أمر إلغاء الكتم (بالرد على الشخص)
    @bot.message_handler(func=lambda m: m.text == "الغاء الكتم")
    def unmute_action(m):
        if m.from_user.id != EMPEROR_ID:
            bot.reply_to(m, "⚠️ أنت عبد من عباد الإمبراطور، لا تتجرأ!")
            return

        if m.reply_to_message:
            target_id = m.reply_to_message.from_user.id
            target_name = m.reply_to_message.from_user.first_name
            
            db_manager.unmute_user(target_id)
            bot.reply_to(m, f"🕊️ عفو إمبراطوري! تم رفع الكتم عن {target_name}.")
        else:
            bot.reply_to(m, "👑 يا إمبراطور، الرد مطلوب لتحديد الشخص.")

    # 📜 قائمة المكتومين
    @bot.message_handler(func=lambda m: m.text == "قائمة المكتومين")
    def show_muted_list(m):
        if m.from_user.id != EMPEROR_ID: return
        
        muted_list = db_manager.get_all_muted_users()
        if not muted_list:
            return bot.reply_to(m, "📪 لا يوجد أحد في القائمة السوداء حالياً.")

        msg = "📜 **قائمة المبعدين من رحمة الإمبراطور:**\n"
        msg += "━━━━━━━━━━━━━━━\n"
        for u in muted_list:
            msg += f"• {u['name']} (ID: `{u['id']}`)\n"
        msg += "━━━━━━━━━━━━━━━"
        bot.send_message(m.chat.id, msg, parse_mode="Markdown")
