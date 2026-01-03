import db_manager # نفترض وجود دالة للحفظ في السحابة
from telebot import types

EMPEROR_ID = 5860391324

def register_handlers(bot):

    # --- 1. فحص كل رسالة تصل للبوت ---
    @bot.message_handler(func=lambda m: True, content_types=['text', 'photo', 'video', 'sticker'], priority=1)
    def check_if_muted(m):
        # إذا كان الشخص مكتوم في قاعدة البيانات، البوت يتجاهله تماماً
        if db_manager.is_user_muted(m.from_user.id):
            return 
        # إذا لم يكن مكتوماً، يكمل البوت عمله الطبيعي
        pass

    # --- 2. أمر الكتم وإلغاء الكتم ---
    @bot.message_handler(func=lambda m: m.text in ["كتم", "الغاء الكتم"])
    def mute_unmute_logic(m):
        if m.from_user.id != EMPEROR_ID:
            bot.reply_to(m, "⚠️ أنت عبد من عباد الإمبراطور، لا تتجرأ وتقول ذلك ثانية!")
            return

        if not m.reply_to_message:
            bot.reply_to(m, "👑 يا إمبراطور، يجب الرد على رسالة الشخص.")
            return

        target_id = m.reply_to_message.from_user.id
        target_name = m.reply_to_message.from_user.first_name

        if m.text == "كتم":
            db_manager.mute_user(target_id, target_name) # إضافة للقائمة السوداء
            bot.send_message(m.chat.id, f"⚔️ تم كتم {target_name} نهائياً من استخدام البوت بأمر إمبراطوري.")
        
        elif m.text == "الغاء الكتم":
            db_manager.unmute_user(target_id) # إزالة من القائمة السوداء
            bot.send_message(m.chat.id, f"🕊️ تم رفع الكتم عن {target_name}، بفضل عفو الإمبراطور.")

    # --- 3. قائمة المكتومين ---
    @bot.message_handler(func=lambda m: m.text == "قائمة المكتومين")
    def list_muted(m):
        if m.from_user.id != EMPEROR_ID:
            bot.reply_to(m, "⚠️ للعبيد الحق في الصمت، لا في رؤية قوائم الأسياد!")
            return

        muted_users = db_manager.get_all_muted_users() # جلب القائمة من db
        
        if not muted_users:
            return bot.reply_to(m, "📪 لا يوجد أحد في قائمة الكتم حالياً يا إمبراطور.")

        msg = "📜 **قائمة المغضوب عليهم (المكتومين):**\n"
        msg += "━━━━━━━━━━━━━━━\n"
        for user in muted_users:
            msg += f"👤 {user['name']} | ID: `{user['id']}`\n"
        msg += "━━━━━━━━━━━━━━━"
        
        bot.send_message(m.chat.id, msg, parse_mode="Markdown")
