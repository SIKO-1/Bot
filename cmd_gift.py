from datetime import datetime, timedelta
import db_manager # استدعاء الملف بالكامل لضمان عمل الدوال

def register_handlers(bot):
    
    # --- أمر الهدية اليومية ---
    @bot.message_handler(func=lambda message: message.text == "هدية")
    def gift_command(message):
        uid = message.from_user.id
        user = db_manager.get_user(uid) or {} # حماية ضد الانهيار
        now = datetime.now()
        
        # استخدام الحقل الصحيح للوقت
        last_gift_str = user.get("last_gift")
        if last_gift_str:
            try:
                last_time = datetime.fromisoformat(last_gift_str)
                if now < last_time + timedelta(days=1):
                    diff = (last_time + timedelta(days=1)) - now
                    hours, minutes = int(diff.total_seconds() // 3600), int((diff.total_seconds() % 3600) // 60)
                    return bot.reply_to(message, f"🌚 باقيلك {hours} ساعة و {minutes} دقيقة.. لا تصير طماع! امشي العب وحصل ذهب 🏃‍♂️")
            except: pass # في حال وجود خطأ في صيغة التاريخ

        # إضافة الذهب (باستخدام المسميات الصحيحة)
        gold_reward = 500 [cite: 2026-01-02]
        db_manager.update_user_gold(uid, gold_reward)
        db_manager.update_user(uid, {"last_gift": now.isoformat()})
        
        new_gold = db_manager.get_user_gold(uid)
        bot.reply_to(message, f"🎁 هاك هذي 500 ذهبة هدية.. \n💰 صار عندك {new_gold} ذهبة، لا تصرفها كلها!")

    # --- أمر الرصيد ---
    @bot.message_handler(func=lambda message: message.text in ["فلوسي", "رصيدي", "رصيد"])
    def balance_command(message):
        gold = db_manager.get_user_gold(message.from_user.id)
        
        if gold > 1000:
            msg = f"💰 رصيدك: {gold} ذهبة\n🔥 أوهووو! عندك كثير ذهب يا غني! 🤑"
        else:
            msg = f"💰 رصيدك: {gold} ذهبة\n💸 هذي كل فلوسك؟ يا فقير شد حيلك! 🤡"
        bot.reply_to(message, msg)
