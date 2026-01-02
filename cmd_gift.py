import db_manager
from datetime import datetime, timedelta

def register_handlers(bot):
    
    # --- 🎁 1. أمر الهدية اليومية (كامل ومغلق الثغرات) ---
    @bot.message_handler(func=lambda message: message.text == "هدية")
    def gift_command(message):
        uid = message.from_user.id
        
        # جلب البيانات مع حماية ضد الـ None
        user = db_manager.get_user(uid) or {}
        now = datetime.now()
        
        # التحقق من وقت آخر استلام مخزن في السحابة
        last_gift_str = user.get("last_gift")
        
        if last_gift_str:
            try:
                last_time = datetime.fromisoformat(last_gift_str)
                # إذا لم تمر 24 ساعة يرفض الطلب
                if now < last_time + timedelta(days=1):
                    diff = (last_time + timedelta(days=1)) - now
                    hours = int(diff.total_seconds() // 3600)
                    minutes = int((diff.total_seconds() % 3600) // 60)
                    
                    # الرد الفكاهي الذي تريده
                    msg = f"🌚 باقيلك {hours} ساعة و {minutes} دقيقة وتحصل هديتك ثانية.. لا تصير طماع! امشي العب وحصل ذهب ادبسز 🏃‍♂️"
                    return bot.reply_to(message, msg)
            except Exception as e:
                print(f"Error parsing time: {e}")

        # --- تنفيذ عملية الهدية (500 ذهبة) ---
        reward = 500 # [cite: 2026-01-02]
        
        # 1. تحديث الوقت فوراً في السحابة لمنع التكرار
        db_manager.update_user(uid, {"last_gift": now.isoformat()})
        
        # 2. إضافة الذهب للحساب [cite: 2026-01-02]
        db_manager.update_user_gold(uid, reward)
        
        # 3. جلب الرصيد الجديد للعرض
        new_gold = db_manager.get_user_gold(uid)
        
        bot.reply_to(message, f"🎁 هاك هذي 500 ذهبة هدية.. \n💰 صار عندك {new_gold} ذهبة، لا تصرفها كلها مرة وحدة! 😉")

    # --- 💰 2. أمر الرصيد (فلوسي / رصيدي / رصيد) ---
    @bot.message_handler(func=lambda message: message.text in ["فلوسي", "رصيدي", "رصيد"])
    def balance_command(message):
        # جلب الذهب من قاعدة البيانات
        gold = db_manager.get_user_gold(message.from_user.id)
        
        # الردود الحماسية
        if gold > 1000:
            msg = f"💰 رصيدك: {gold} ذهبة\n🔥 أوهووو! عندك كثير ذهب يا غني، من أين لك هذا؟ 🤑"
        else:
            msg = f"💰 رصيدك: {gold} ذهبة\n💸 هذي كل فلوسك؟ يا فقير شد حيلك وجمع ذهب! 🤡"
            
        bot.reply_to(message, msg)
