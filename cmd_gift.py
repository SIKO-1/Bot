import db_manager
from datetime import datetime, timedelta

def register_handlers(bot):
    
    @bot.message_handler(func=lambda message: message.text == "هدية")
    def gift_command(message):
        uid = message.from_user.id
        
        # 1. جلب البيانات مع حماية ضد الـ None
        user = db_manager.get_user(uid)
        if not user:
            # إذا كان المستخدم جديد تماماً، نقوم بتسجيله أولاً
            db_manager.update_user(uid, {"gold": 0, "last_gift": "2000-01-01T00:00:00"})
            user = {"gold": 0, "last_gift": "2000-01-01T00:00:00"}

        now = datetime.now()
        
        # 2. التحقق من الوقت بطريقة آمنة
        last_gift_str = user.get("last_gift")
        try:
            if last_gift_str:
                # تحويل النص إلى وقت (يدوياً لضمان التوافق)
                last_time = datetime.strptime(last_gift_str.split(".")[0], "%Y-%m-%dT%HH:%MM:%SS") if "T" in last_gift_str else datetime.min
                
                if now < last_time + timedelta(days=1):
                    diff = (last_time + timedelta(days=1)) - now
                    hours = int(diff.total_seconds() // 3600)
                    minutes = int((diff.total_seconds() % 3600) // 60)
                    return bot.reply_to(message, f"🌚 باقيلك {hours} ساعة و {minutes} دقيقة وتحصل هديتك ثانية..")
        except Exception as e:
            print(f"Time error: {e}") # لن ينهار البوت، سيكمل العملية

        # 3. إضافة الذهب (تأكد من استخدام 'gold' وليس 'balance') [cite: 2026-01-02]
        reward = 500
        db_manager.update_user_gold(uid, reward)
        # حفظ الوقت بصيغة نصية بسيطة
        db_manager.update_user(uid, {"last_gift": now.strftime("%Y-%m-%dT%H:%M:%S")})
        
        # جلب الرصيد الجديد للعرض
        new_gold = db_manager.get_user_gold(uid)
        bot.reply_to(message, f"🎁 هاك هذي {reward} ذهبة هدية..\n💰 صار عندك {new_gold} ذهبة!")

    @bot.message_handler(func=lambda message: message.text in ["فلوسي", "رصيدي", "رصيد"])
    def balance_command(message):
        gold = db_manager.get_user_gold(message.from_user.id)
        bot.reply_to(message, f"💰 رصيدك الحالي: {gold} ذهبة.")
