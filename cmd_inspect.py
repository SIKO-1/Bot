import db_manager

# المعرف الخاص بك يا إمبراطور
ADMIN_ID = 5860391324

def register_handlers(bot):

    @bot.message_handler(func=lambda m: m.text.startswith("كشف حساب") or m.text.startswith("بحث"))
    def inspect_user(m):
        # قصر الصلاحية على الإمبراطور فقط
        if m.from_user.id != ADMIN_ID:
            return bot.reply_to(m, "هذا السجل مخصص لاطلاع الإمبراطور فقط")

        target_id = None
        target_name = None

        # البحث عبر الرد
        if m.reply_to_message:
            target_id = m.reply_to_message.from_user.id
            target_name = m.reply_to_message.from_user.first_name
        
        # البحث عبر المعرف الرقمي
        else:
            parts = m.text.split()
            if len(parts) > 1:
                if parts[1].isdigit():
                    target_id = int(parts[1])
                    # محاولة جلب الاسم إذا كان الشخص مسجلاً في قاعدة البيانات
                    target_data = db_manager.get_user(target_id)
                    target_name = f"صاحب المعرف {target_id}"
                else:
                    return bot.reply_to(m, "يرجى إدخال معرف رقمي صحيح")
            else:
                return bot.reply_to(m, "يتوجب عليكم الرد على رسالة أو كتابة المعرف الرقمي")

        user_data = db_manager.get_user(target_id)
        gold = user_data.get("gold", 0)
        msgs = user_data.get("messages", 0)
        status = "منفي من الديار" if user_data.get("banned") else "مواطن في الخدمة"
        rank = user_data.get("rank", "مواطن")
        
        report = (
            "╔═════════════════╗\n"
            "    وثيقة بيان الحالة \n"
            "╚═════════════════╝\n\n"
            f"بيانات العضو : {target_name}\n"
            "━━━━━━━━━━━━━━━\n\n"
            "سجلات المواطنة :\n"
            "┌──────────────┐\n"
            f"  -- المعرف : {target_id}\n"
            f"  -- الرتبة : {rank}\n"
            f"  -- الذهب : {gold}\n"
            f"  -- الرسائل : {msgs}\n"
            "└──────────────┘\n\n"
            "الشؤون القانونية\n"
            f"   -- الحالة : {status}\n\n"
            "━━━━━━━━━━━━━━━\n"
            "صدرت من ديوان الإمبراطورية\n"
            "━━━━━━━━━━━━━━━\n"
            "تخضع الرعايا لهيبتك"
        )

        bot.reply_to(m, report)
