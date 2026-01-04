import db_manager
import random

def register_handlers(bot):

    @bot.message_handler(func=lambda m: m.text == "مستواي")
    def check_level(m):
        level, xp = db_manager.get_user_level(m.from_user.id)
        
        response = (
            "╔═════════════════╗\n"
            "    سجل الوقار الملكي \n"
            "╚═════════════════╝\n\n"
            f"المحارب: {m.from_user.first_name}\n"
            f"المستوى الحالي: {level}\n"
            f"نقاط الخبرة: {xp}\n"
            "━━━━━━━━━━━━━━━\n"
            "استمر في العطاء ليرتقي شأنك"
        )
        bot.reply_to(m, response)

    @bot.message_handler(func=lambda m: True)
    def track_activity(m):
        # منع البوت من منح نقاط لنفسه أو للأوامر
        if m.text and not m.text.startswith("/") and len(m.text) > 3:
            # منح من 5 إلى 15 نقطة خبرة بشكل عشوائي لكل رسالة
            added_xp = random.randint(5, 15)
            db_manager.update_user_experience(m.from_user.id, added_xp)
