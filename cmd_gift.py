import db_manager
from datetime import datetime, timedelta

def register_handlers(bot):
    @bot.message_handler(func=lambda m: m.text == "هدية")
    def gift(m):
        uid = m.from_user.id
        user = db_manager.get_user(uid)
        now = datetime.now()
        
        # منع التكرار (حل مشكلة الصورة)
        last = user.get("last_gift")
        if last and now < datetime.fromisoformat(last) + timedelta(hours=24):
            return bot.reply_to(m, "Wait! 🌚 ارجع بعدين يا طماع.")

        db_manager.update_user_gold(uid, 500)
        db_manager.update_user(uid, {"last_gift": now.isoformat()})
        gold = db_manager.get_user_gold(uid)
        bot.reply_to(m, f"🎁 مبروك الـ 500!\n💰 رصيدك الحقيقي: {gold}")

    @bot.message_handler(func=lambda m: m.text == "فلوسي")
    def balance(m):
        gold = db_manager.get_user_gold(m.from_user.id)
        bot.reply_to(m, f"💰 رصيدك الحالي: {gold} ذهبة.")
