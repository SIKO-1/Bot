from telebot import types

# هذا الملف يبدأ بـ cmd ليتوافق مع نظام التحميل التلقائي في بوتك
def register_handlers(bot):

    # الأوامر المشغلة للقائمة
    @bot.message_handler(func=lambda m: m.text in ["ادارة", "امبراطورية"])
    def emperor_management(m):
        user_id = m.from_user.id
        user_name = m.from_user.first_name
        
        # تاك الإمبراطور (المنشن)
        emperor_tag = f"[{user_name}](tg://user?id={user_id})"

        # التصميم الإمبراطوري المطلوب
        text = (
            "╔═════════════════╗\n"
            "    إدارة الإمبراطورية \n"
            "╚═════════════════╝\n\n"
            f"مرحباً بك يا امبراطور : {emperor_tag}\n"
            "━━━━━━━━━━━━━━━\n\n"
            "أقسام الإدارة :\n"
            "┌──────────────┐\n"
            "   --  كتم / الغاء الكتم\n"
            "   --   حظر / الغاء الحظر\n"
            "   --  تقيد / الغاء التقيد \n"
            "   --  رفع ادمن / تنزيل admin\n"
            "   -- شحن رصيد / تصفير رصيد شخص\n"
            "   -- تحويل رصيد \n"
            "└──────────────┘\n\n"
            "━━━━━━━━━━━━━━━\n"
            "« **هيبتك لا تُصنع بالخوف، بل بالعدل الذي يرتجف منه الظالم ويطمئن إليه المظلوم.** »"
        )

        bot.send_message(m.chat.id, text, parse_mode="Markdown")
