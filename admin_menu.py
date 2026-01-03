import random
from telebot import types

# هذا الملف سيتم التعرف عليه تلقائياً بواسطة main.py
def register_handlers(bot):

    @bot.message_handler(func=lambda m: m.text in ["ادارة", "امبراطورية"])
    def admin_panel(m):
        # التحقق من الرتبة (تأكد أن رتبتك مسجلة في البوت كمالك)
        user_id = m.from_user.id
        user_name = m.from_user.first_name
        
        # منشن الإمبراطور (تاك)
        mention = f"[{user_name}](tg://user?id={user_id})"

        # التصميم الإمبراطوري الذي طلبته
        text = (
            "╔═════════════════╗\n"
            "    إدارة الإمبراطورية \n"
            "╚═════════════════╝\n\n"
            f"مرحباً بك يا امبراطور : {mention}\n"
            "━━━━━━━━━━━━━━━\n\n"
            "أقسام الإدارة :\n"
            "┌──────────────┐\n"
            "   --  كتم / الغاء الكتم\n"
            "   --   حظر / الغاء الحظر\n"
            "   --  تقيد / الغاء التقيد \n"
            "   --  رفع ادمن / تنزيل ادمن \n"
            "   -- شحن رصيد / تصفير رصيد شخص\n"
            "   -- تحويل رصيد \n"
            "└──────────────┘\n\n"
            "━━━━━━━━━━━━━━━\n"
            "« **تاجك الحكمة، وسيفك الحزم، ومن نال عفوك فقد نال حياة جديدة.** »"
        )

        bot.send_message(m.chat.id, text, parse_mode="Markdown")
