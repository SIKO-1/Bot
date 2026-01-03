import db_manager
from datetime import datetime, timedelta

def register_handlers(bot):
    @bot.message_handler(func=lambda m: m.text == "هدية")
    def gift_cmd(m):
        uid = m.from_user.id
        user = db_manager.get_user(uid) or {}
        now = datetime.now()
        
        last_gift = user.get("last_gift")
        if last_gift:
            try:
                last_time = datetime.fromisoformat(last_gift)
                if now < last_time + timedelta(days=1):
                    diff = (last_time + timedelta(days=1)) - now
                    h = int(diff.total_seconds() // 3600)
                    return bot.reply_to(m, f"🌚 باقيلك {h} ساعة.. لا تصير طماع ادبسز! 🏃‍♂️")
            except: pass

        db_manager.update_user_gold(uid, 500)
        db_manager.update_user(uid, {"last_gift": now.isoformat()})
        gold = db_manager.get_user_gold(uid)
        bot.reply_to(m, f"🎁 مبروك الـ 500 ذهبة!\n💰 رصيدك الآن: {gold}")

    @bot.message_handler(func=lambda m: m.text in ["فلوسي", "رصيدي", "رصيد"])
    def bal_cmd(m):
        gold = db_manager.get_user_gold(m.from_user.id)
        bot.reply_to(m, f"💰 رصيدك: {gold} ذهبة.")
