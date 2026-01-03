import db_manager
from datetime import datetime, timedelta

def register_handlers(bot):
    print("💎 نظام الهدايا والذهب تم تحميله بنجاح!")

    @bot.message_handler(func=lambda m: m.text == "هدية")
    def gift_handle(m):
        try:
            uid = m.from_user.id
            user = db_manager.get_user(uid)
            now = datetime.now()

            # التحقق من الوقت
            last_gift = user.get("last_gift")
            if last_gift:
                last_time = datetime.fromisoformat(last_gift)
                if now < last_time + timedelta(hours=24):
                    diff = (last_time + timedelta(hours=24)) - now
                    h, rem = divmod(int(diff.total_seconds()), 3600)
                    return bot.reply_to(m, f"🌚 باقيلك {h} ساعة و {rem//60} دقيقة.. لا تصير طماع! 🏃‍♂️")

            # إضافة الذهب (داخلياً)
            db_manager.update_user_gold(uid, 500)
            db_manager.update_user(uid, {"last_gift": now.isoformat()})
            
            gold = db_manager.get_user_gold(uid)
            bot.reply_to(m, f"🎁 مبروك الـ 500 ذهبة!\n💰 رصيدك الآن: {gold}")
        except Exception as e:
            print(f"❌ خطأ في أمر هدية: {e}")

    @bot.message_handler(func=lambda m: m.text in ["فلوسي", "رصيدي", "رصيد"])
    def bal_handle(m):
        try:
            gold = db_manager.get_user_gold(m.from_user.id)
            bot.reply_to(m, f"💰 رصيدك الحالي: {gold} ذهبة.")
        except Exception as e:
            print(f"❌ خطأ في أمر الرصيد: {e}")
