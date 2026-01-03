import db_manager
from datetime import datetime, timedelta

def register_handlers(bot):
    
    # --- 🎁 نظام الهدية اليومية ---
    @bot.message_handler(func=lambda m: m.text == "هدية")
    def gift_handle(m):
        uid = m.from_user.id
        user = db_manager.get_user(uid)
        now = datetime.now()

        # التحقق من الوقت (قفل ثغرة التكرار)
        last_gift = user.get("last_gift")
        if last_gift:
            try:
                last_time = datetime.fromisoformat(last_gift)
                if now < last_time + timedelta(hours=24):
                    diff = (last_time + timedelta(hours=24)) - now
                    h = int(diff.total_seconds() // 3600)
                    m_rem = int((diff.total_seconds() % 3600) // 60)
                    return bot.reply_to(m, f"🌚 باقيلك {h} ساعة و {m_rem} دقيقة.. لا تصير طماع! 🏃‍♂️")
            except: pass

        # إضافة الذهب وتحديث الوقت داخلياً
        db_manager.update_user_gold(uid, 500)
        db_manager.update_user(uid, {"last_gift": now.isoformat()})
        
        # جلب الرصيد الحقيقي من الذاكرة
        gold = db_manager.get_user_gold(uid)
        bot.reply_to(m, f"🎁 مبروك الـ 500 ذهبة يا إمبراطور!\n💰 رصيدك الآن: {gold}")

    # --- 💰 نظام عرض الرصيد ---
    @bot.message_handler(func=lambda m: m.text in ["فلوسي", "رصيدي", "رصيد"])
    def bal_handle(m):
        gold = db_manager.get_user_gold(m.from_user.id)
        if gold > 5000:
            status = "🔥 يا غني الإمبراطورية!"
        elif gold > 1000:
            status = "✨ وضعك مستور.."
        else:
            status = "💸 شد حيلك يا فقير! 🤡"
            
        bot.reply_to(m, f"💰 رصيدك الحالي: {gold} ذهبة.\n{status}")
