import db_manager
from datetime import datetime, timedelta

def register_handlers(bot):

    @bot.message_handler(func=lambda m: m.text == "هدية")
    def gift_handle(m):
        uid = m.from_user.id
        user = db_manager.get_user(uid) or {}
        now = datetime.now()

        # فحص الوقت
        last_gift = user.get("last_gift")
        if last_gift:
            last_time = datetime.fromisoformat(last_gift)
            if now < last_time + timedelta(hours=24):
                diff = (last_time + timedelta(hours=24)) - now
                h, rem = divmod(int(diff.total_seconds()), 3600)
                m_curr = rem // 60
                return bot.reply_to(m, f"🌚 باقيلك {h} ساعة و {m_curr} دقيقة.. لا تصير طماع ادبسز! 🏃‍♂️")

        # إضافة الذهب (500) وتحديث الوقت [cite: 2026-01-02]
        db_manager.update_user_gold(uid, 500)
        db_manager.update_user(uid, {"last_gift": now.isoformat()})
        
        # التأكد من الرصيد الجديد
        new_gold = db_manager.get_user_gold(uid)
        bot.reply_to(m, f"🎁 هاك هذي 500 ذهبة هدية..\n💰 صار عندك {new_gold} ذهبة!")

    @bot.message_handler(func=lambda m: m.text in ["فلوسي", "رصيد", "رصيدي"])
    def balance_handle(m):
        gold = db_manager.get_user_gold(m.from_user.id)
        if gold > 1000:
            msg = f"💰 رصيدك: {gold} ذهبة\n🔥 أوهووو! عندك كثير ذهب يا غني! 🤑"
        else:
            msg = f"💰 رصيدك: {gold} ذهبة\n💸 هذي كل فلوسك؟ يا فقير شد حيلك! 🤡"
        bot.reply_to(m, msg)
