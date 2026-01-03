import db_manager
from datetime import datetime, timedelta

def register_handlers(bot):
    @bot.message_handler(func=lambda m: m.text == "هدية")
    def gift_handle(m):
        uid = m.from_user.id
        user = db_manager.get_user(uid)
        now = datetime.now()

        # قفل الثغرة: التحقق من الوقت
        last_gift = user.get("last_gift")
        if last_gift:
            try:
                last_time = datetime.fromisoformat(last_gift)
                if now < last_time + timedelta(hours=24):
                    diff = (last_time + timedelta(hours=24)) - now
                    h = int(diff.total_seconds() // 3600)
                    return bot.reply_to(m, f"🌚 باقيلك {h} ساعة.. لا تصير طماع ادبسز! 🏃‍♂️")
            except: pass

        # تنفيذ الإضافة الحقيقية في السحابة [cite: 2026-01-02]
        db_manager.update_user_gold(uid, 500)
        db_manager.update_user(uid, {"last_gift": now.isoformat()})
        
        # جلب الرصيد بعد التحديث للتأكد
        gold = db_manager.get_user_gold(uid)
        bot.reply_to(m, f"🎁 مبروك الـ 500 ذهبة!\n💰 رصيدك الحقيقي الآن: {gold}")

    @bot.message_handler(func=lambda m: m.text in ["فلوسي", "رصيدي", "رصيد"])
    def balance_handle(m):
        gold = db_manager.get_user_gold(m.from_user.id)
        bot.reply_to(m, f"💰 رصيدك الحالي: {gold} ذهبة.")
