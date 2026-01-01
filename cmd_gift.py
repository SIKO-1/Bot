from datetime import datetime, timedelta
from db_manager import get_user, update_user

def register_gift_handler(bot):
    @bot.message_handler(func=lambda m: m.text == "هدية")
    def gift(m):
        user = get_user(m.from_user.id)
        now = datetime.now()
        if user.get("last_gift"):
            last = datetime.fromisoformat(user["last_gift"])
            if now < last + timedelta(days=1):
                return bot.reply_to(m, "❌ استلمتها سابقاً!")
        
        update_user(m.from_user.id, "balance", user["balance"] + 500)
        update_user(m.from_user.id, "last_gift", now.isoformat())
        bot.reply_to(m, "🎁 حصلت على 500 نقطة!")

    @bot.message_handler(func=lambda m: m.text == "فلوسي")
    def balance(m):
        user = get_user(m.from_user.id)
        bot.reply_to(m, f"💰 رصيدك: {user['balance']}")
