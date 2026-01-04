import db_manager

# معرف الإمبراطور (أنت)
EMPEROR_ID = 5860391324

def register_handlers(bot):

    @bot.message_handler(func=lambda m: m.text and m.text.startswith("اضف امر "))
    def add_custom_command(m):
        user_id = m.from_user.id
        chat_id = m.chat.id
        
        # 1. التحقق إذا كان المستخدم هو الإمبراطور
        is_emperor = (user_id == EMPEROR_ID)
        
        # 2. التحقق إذا كان المستخدم مشرفاً في المجموعة
        user_status = bot.get_chat_member(chat_id, user_id).status
        is_admin = user_status in ['administrator', 'creator']

        # إذا لم يكن إمبراطوراً ولا مشرفاً، يتم رفض الطلب
        if not (is_emperor or is_admin):
            return bot.reply_to(m, "هذا المرسوم لا يصدر إلا عن الإمبراطور أو ولاته المقربين.")

        try:
            # تقسيم النص: اضف امر [الكلمة] [الرد]
            parts = m.text.split(" ", 3)
            if len(parts) < 4:
                bot.reply_to(m, "الصيغة الملكية هي: اضف امر (الكلمة) (الرد)")
                return

            cmd_name = parts[2]
            cmd_reply = parts[3]

            # تخزين الأمر في الديوان السحابي
            db_manager.save_custom_command(cmd_name, cmd_reply)
            
            bot.reply_to(m, f"تم اعتماد المرسوم الجديد بنجاح\nالكلمة: {cmd_name}\nالرد: {cmd_reply}")
        except Exception as e:
            bot.reply_to(m, f"حدث اضطراب أثناء تسجيل المرسوم: {e}")

    @bot.message_handler(func=lambda m: True)
    def handle_all_messages(m):
        # البحث عن الأوامر المضافة مسبقاً في السحاب
        if m.text:
            reply = db_manager.get_custom_command(m.text)
            if reply:
                bot.reply_to(m, reply)
