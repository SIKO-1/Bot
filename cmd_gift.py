import db_manager
from datetime import datetime, timedelta

def register_handlers(bot):
    @bot.message_handler(func=lambda m: m.text == "هدية")
    def gift(m):
        uid = m.from_user.id
        # جلب البيانات مرة واحدة فقط في البداية
        user = db_manager.get_user(uid)
        
        # حارس الحظر
        if user.get("banned"):
            return

        now = datetime.now()
        
        # نظام التحقق من الوقت
        last = user.get("last_gift")
        if last:
            try:
                last_time = datetime.fromisoformat(last)
                if now < last_time + timedelta(hours=24):
                    remaining = (last_time + timedelta(hours=24)) - now
                    hours = remaining.seconds // 3600
                    return bot.reply_to(m, f"⚠️ ارجع بعد {hours} ساعة يا طماع! 🌚")
            except:
                pass # في حال وجود خطأ في تنسيق التاريخ القديم

        # --- العملية الحاسمة: إضافة الذهب وحفظ التاريخ معاً ---
        current_gold = user.get("gold", 0)
        new_gold = current_gold + 500
        
        # تحديث شامل في أمر واحد لضمان عدم ضياع البيانات
        db_manager.update_user(uid, {
            "gold": new_gold,
            "last_gift": now.isoformat()
        })

        bot.reply_to(m, f"🎁 مبروك يا إمبراطور.. استلمت 500 قطعة!\n💰 رصيدك الآن: {new_gold}")

    @bot.message_handler(func=lambda m: m.text == "فلوسي")
    def balance(m):
        # جلب الذهب مباشرة من الخزينة
        gold = db_manager.get_user_gold(m.from_user.id)
        bot.reply_to(m, f"💰 رصيدك الحالي في الخزينة: {gold} ذهبة.")
