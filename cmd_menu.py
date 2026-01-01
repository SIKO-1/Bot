from db_manager import get_user

def register_handlers(bot):
    # الآيدي الخاص بك كإمبراطور
    DEV_ID = 5860391324

    @bot.message_handler(func=lambda message: message.text in ["اوامر", "الأوامر", "الاوامر", "قائمة"])
    def luxury_menu(message):
        name = message.from_user.first_name
        user_id = message.from_user.id
        
        menu_text = (
            f"✨ **أهلاً بك يا {name} في العرش الإمبراطوري** ✨\n"
            "▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
            "📜 **قائمة الأقسام الملكية**\n"
            "▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\n"
            "🎮 **🕹 الألعاب**\n\n"
            "🛒 **🏬 المتجر**\n\n"
        )

        # قسم الإمبراطورية يظهر لك أنت فقط
        if user_id == DEV_ID:
            menu_text += "🏰 **👑 الإمبراطورية**\n\n"
        
        menu_text += (
            "▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
            "🆔 ارسل `ايدي` لعرض بطاقتك الشخصية\n"
            "▬▬▬▬▬▬▬▬▬▬▬▬▬▬"
        )
        
        bot.reply_to(message, menu_text, parse_mode="Markdown")

    @bot.message_handler(func=lambda message: message.text == "ايدي")
    def luxury_id(message):
        uid = message.from_user.id
        name = message.from_user.first_name
        user_data = get_user(uid) # جلب البيانات من الذاكرة الدائمة
        
        points = user_data.get("balance", 0)
        rank = user_data.get("rank", "عضو")
        
        # تحديد رسالة التنمر أو المدح حسب النقاط
        if points > 1000:
            comment = "🔥 أوه، الإمبراطورية فخورة بك يا غني!"
        else:
            comment = "🤡 يا فقير، اذهب واجمع بعض النقاط قبل أن أطردك!"

        # محاولة جلب صورة البروفايل
        try:
            photos = bot.get_user_profile_photos(uid)
            if photos.total_count > 0:
                # إذا عنده صورة يرسلها مع البيانات
                photo_id = photos.photos[0][-1].file_id
                caption = (
                    f"✨ **بطاقة الهوية الإمبراطورية** ✨\n"
                    f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
                    f"👤 **الاسم:** {name}\n"
                    f"🆔 **الآيدي:** `{uid}`\n"
                    f"💰 **النقاط:** {points}\n"
                    f"🎖 **الرتبة:** {rank}\n"
                    f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
                    f"💬 {comment}"
                )
                bot.send_photo(message.chat.id, photo_id, caption=caption, parse_mode="Markdown")
            else:
                raise Exception("No Photo")
        except:
            # إذا ما عنده صورة أو حدث خطأ يرسل نص فقط
            id_card = (
                f"👤 **الاسم:** {name}\n"
                f"🆔 **الآيدي:** `{uid}`\n"
                f"💰 **النقاط:** {points}\n"
                f"🎖 **الرتبة:** {rank}\n\n"
                f"💬 {comment}"
            )
            bot.reply_to(message, id_card, parse_mode="Markdown")
