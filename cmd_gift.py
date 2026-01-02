import db_manager
from datetime import datetime, timedelta

def register_handlers(bot):
    
    # --- 🎁 1. أمر الهدية (إصلاح الرصيد والوقت) ---
    @bot.message_handler(func=lambda message: message.text == "هدية")
    def gift_command(message):
        uid = message.from_user.id
        # جلب البيانات من السحابة (استخدام gold حصراً)
        user = db_manager.get_user(uid) or {}
        now = datetime.now()
        
        # فحص الوقت لمنع التكرار
        last_gift_str = user.get("last_gift")
        if last_gift_str:
            try:
                last_time = datetime.fromisoformat(last_gift_str)
                if now < last_time + timedelta(days=1):
                    diff = (last_time + timedelta(days=1)) - now
                    hours, minutes = int(diff.total_seconds() // 3600), int((diff.total_seconds() % 3600) // 60)
                    msg = f"🌚 باقيلك {hours} ساعة و {minutes} دقيقة وتحصل هديتك ثانية.. لا تصير طماع ادبسز! 🏃‍♂️"
                    return bot.reply_to(message, msg)
            except: pass

        # إضافة الذهب الحقيقي للسحابة (500 ذهبة) [cite: 2026-01-02]
        db_manager.update_user_gold(uid, 500)
        # تحديث وقت الاستلام فوراً
        db_manager.update_user(uid, {"last_gift": now.isoformat()})
        
        # جلب الرصيد الجديد بعد التحديث
        new_gold = db_manager.get_user_gold(uid)
        bot.reply_to(message, f"🎁 هاك هذي 500 ذهبة هدية..\n💰 صار عندك {new_gold} ذهبة، لا تصرفها كلها مرة وحدة! 😉")

    # --- 💰 2. أمر الرصيد (فلوسي / رصيدي / رصيد) ---
    @bot.message_handler(func=lambda message: message.text in ["فلوسي", "رصيدي", "رصيد"])
    def balance_command(message):
        gold = db_manager.get_user_gold(message.from_user.id)
        
        if gold > 1000:
            msg = f"💰 رصيدك: {gold} ذهبة\n🔥 أوهووو! عندك كثير ذهب يا غني، من أين لك هذا؟ 🤑"
        else:
            msg = f"💰 رصيدك: {gold} ذهبة\n💸 هذي كل فلوسك؟ يا فقير شد حيلك وجمع ذهب! 🤡"
        bot.reply_to(message, msg)
