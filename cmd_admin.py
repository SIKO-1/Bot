from telebot import types

# ضع الـ ID الخاص بك هنا ليعرف البوت أنك الإمبراطور
EMPEROR_ID = 5860391324  # <--- استبدل هذا الرقم بـ ID حسابك الحقيقي

def register_handlers(bot):

    @bot.message_handler(func=lambda m: m.text in ["ادارة", "امبراطورية"])
    def emperor_only_panel(m):
        user_id = m.from_user.id
        user_name = m.from_user.first_name

        # 1. إذا كان الشخص هو الإمبراطور (أنت)
        if user_id == EMPEROR_ID:
            emperor_tag = f"[{user_name}](tg://user?id={user_id})"
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
                "   --  روح / سجل البوت \n" 
                "   --  رفع ادمن / تنزيل admin\n"
                "   -- شحن رصيد / تصفير رصيد شخص\n"
                "   -- تحويل رصيد \n"
                "└──────────────┘\n\n"
                "━━━━━━━━━━━━━━━\n"
                "« **هيبتك لا تُصنع بالخوف، بل بالعدل الذي يرتجف منه الظالم.** »"
            )
            bot.send_message(m.chat.id, text, parse_mode="Markdown")
        
        # 2. إذا كان أي شخص آخر (العبيد)
        else:
            bot.reply_to(m, "⚠️ أنت عبد من عباد الإمبراطور، لا تتجرأ وتقول ذلك ثانية!")

